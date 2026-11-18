"""strata-worker MCP 서버 (stdio, 줄 단위 JSON-RPC 2.0). 외부 패키지 없이 표준 라이브러리만 쓴다.

지휘자(Claude Code · Codex)가 이 서버를 MCP 로 붙이면 도구 3개가 생긴다:
  delegate_code_task  작은 코딩 작업 하나를 로컬 LLM(STRATA)에 맡기고 diff · 테스트 결과를 받는다
  worker_status       서버 연결 · 잠금 · 설정 · 남은 작업 트리
  discard_worktree    끝난 작업 트리 삭제

노트북에서는 ssh 로 본체의 이 파일을 실행한다 (docs/WORKER.md). 표준 출력은 프로토콜 전용이라 진단은 표준 오류로만 쓴다.
"""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

PROTO = "2025-06-18"
TOOLS = [
    {"name": "delegate_code_task",
     "description": ("작은 코딩 작업 하나를 본체 로컬 LLM(Qwen3.6-35B-A3B, STRATA, 32K)에 맡긴다. 맞는 크기: 파일 1~3개, 수십 줄, "
                     "할 일 · 경계 조건 · 확인 방법이 분명한 티켓. 설계 · 여러 모듈 리팩터링 · 디버깅 조사는 맡기지 말 것. "
                     "저장소의 커밋된 상태(ref)를 별도 작업 트리로 꺼내 수정하고 unified diff 를 돌려준다. 원본 작업 트리는 바뀌지 않으므로 "
                     "결과를 검토한 뒤 직접 git apply 한다. 한 번에 한 작업만 돌고 수 분이 걸릴 수 있다."),
     "inputSchema": {"type": "object", "properties": {
         "task": {"type": "string", "description": "할 일. 바꿀 함수 · 기대 동작 · 예외 · 경계 조건까지 구체적으로"},
         "repo": {"type": "string", "description": "본체(desktop-5070)의 git 저장소 경로(예: C:\\strata-lab) 또는 clone 할 git URL"},
         "ref": {"type": "string", "description": "기준 커밋 · 브랜치 (기본 HEAD). 노트북 변경은 먼저 push 해야 보인다"},
         "files": {"type": "array", "items": {"type": "string"}, "description": "먼저 볼 파일 (저장소 루트 기준)"},
         "test_cmd": {"type": "string", "description": "작업 트리에서 돌릴 확인 명령(cmd.exe). 0 으로 끝나면 통과. 실패하면 로그로 1회 보완"},
         "max_steps": {"type": "integer", "description": "도구 루프 최대 턴 (기본 20)"},
         "repair": {"type": "boolean", "description": "테스트 실패 시 1회 보완 (기본 true)"},
         "keep_worktree": {"type": "boolean", "description": "끝난 뒤 작업 트리를 남길지 (기본 true)"}},
         "required": ["task", "repo"]}},
    {"name": "worker_status", "description": "STRATA 서버 연결 · 작업 중 여부 · 워커 설정 · 남은 작업 트리",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "discard_worktree", "description": "delegate_code_task 가 남긴 작업 트리를 지운다",
     "inputSchema": {"type": "object", "properties": {"worker_id": {"type": "string"}}, "required": ["worker_id"]}},
]


def log(*a):
    print("[strata-worker]", *a, file=sys.stderr, flush=True)


def call_tool(name: str, args: dict) -> tuple[dict, bool]:
    import strata_worker as w
    if name == "delegate_code_task":
        allowed = {"task", "repo", "ref", "files", "test_cmd", "max_steps", "repair", "keep_worktree"}
        r = w.delegate(**{k: v for k, v in args.items() if k in allowed})
        return r, r.get("status") not in ("done", "no_change", "tests_failed")
    if name == "worker_status":
        return w.status(), False
    if name == "discard_worktree":
        wid = str(args.get("worker_id", ""))
        if not wid or any(c in wid for c in "\\/.:"):
            return {"error": "worker_id 형식이 아니다"}, True
        return {"worker_id": wid, "result": w.drop_tree(wid)}, False
    return {"error": f"알 수 없는 도구 {name}"}, True


def handle(req: dict) -> dict | None:
    mid, method, params = req.get("id"), req.get("method", ""), req.get("params") or {}
    if mid is None:          # 알림 (notifications/initialized 등)
        return None
    if method == "initialize":
        res = {"protocolVersion": params.get("protocolVersion") or PROTO, "capabilities": {"tools": {"listChanged": False}},
               "serverInfo": {"name": "strata-worker", "version": "0.1.0"}}
    elif method == "ping":
        res = {}
    elif method == "tools/list":
        res = {"tools": TOOLS}
    elif method == "tools/call":
        try:
            out, is_err = call_tool(params.get("name", ""), params.get("arguments") or {})
        except Exception:  # noqa: BLE001
            out, is_err = {"error": traceback.format_exc()[-1500:]}, True
        res = {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False, indent=1)}], "isError": is_err}
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": res}


def main() -> int:
    stdin = open(sys.stdin.fileno(), "r", encoding="utf-8", newline="\n", closefd=False)
    stdout = open(sys.stdout.fileno(), "w", encoding="utf-8", newline="\n", closefd=False)
    sys.stdout = sys.stderr            # 혹시 모를 print 가 프로토콜을 깨지 않게
    log("ready")
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}) + "\n")
            stdout.flush()
            continue
        for r in (req if isinstance(req, list) else [req]):
            resp = handle(r)
            if resp is not None:
                stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
                stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
