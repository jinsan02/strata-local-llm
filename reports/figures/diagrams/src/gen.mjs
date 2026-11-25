// STRATA 구조도 4장을 Excalidraw 파일(.excalidraw)로 만든다. node gen.mjs
// Tiny Lab 톤: 종이색 바탕 · 파스텔 칸 · Lucide 아이콘 · 나눔손글씨 펜(render.html 이 글꼴을 입힌다).
// 상자 안 글자는 핵심 몇 단어만, 자세한 설명은 위키로.
import { writeFileSync } from "node:fs";

const C = { violet: "#e5dbff", blue: "#d0ebff", green: "#d3f9d8", yellow: "#fff3bf", red: "#ffe3e3", gray: "#f1f3f5", white: "#ffffff" };
const DEEP = { "#e5dbff": "#6741d9", "#d0ebff": "#1971c2", "#d3f9d8": "#2f9e44", "#fff3bf": "#e67700", "#ffe3e3": "#c92a2a", "#f1f3f5": "#495057", "#ffffff": "#343a40" };
const INK = "#343a40", RED = "#e03131", MUTED = "#adb5bd", SUB = "#495057";
const S = { title: 52, sub: 30, head: 38, body: 31, label: 28, frame: 30 };
let seed = 1000;
const nid = (p) => `${p}-${++seed}`;
const base = (o) => ({ angle: 0, strokeColor: INK, backgroundColor: "transparent", fillStyle: "solid", strokeWidth: 2, strokeStyle: "solid",
  roughness: 1, opacity: 100, groupIds: [], frameId: null, roundness: null, seed: ++seed, version: 1, versionNonce: ++seed, isDeleted: false,
  boundElements: null, updated: 1, link: null, locked: false, ...o });
const cw = (ch, s) => (/[ㄱ-힝]/.test(ch) ? s * 0.8 : s * 0.45);
const tw = (line, s) => [...line].reduce((a, ch) => a + cw(ch, s), 0);

function text(x, y, t, { size = S.body, align = "center", color = INK } = {}) {
  const lines = t.split("\n");
  const width = Math.max(...lines.map((l) => tw(l, size)));
  const height = lines.length * size * 1.25;
  return base({ id: nid("t"), type: "text", x: align === "center" ? x - width / 2 : x, y, width, height, text: t, originalText: t,
    fontSize: size, fontFamily: 2, textAlign: align, verticalAlign: "top", baseline: size, containerId: null, lineHeight: 1.25,
    strokeColor: color, autoResize: true });
}

function box(x, y, w, h, head, body, { fill = C.white, dashed = false, stroke = INK, icon } = {}) {
  const r = base({ id: nid("r"), type: "rectangle", x, y, width: w, height: h, backgroundColor: fill, roundness: { type: 3 },
    strokeStyle: dashed ? "dashed" : "solid", strokeColor: stroke });
  const out = [r], ids = [];
  if (head) { const hl = text(x + w / 2, y, head, { size: S.head }); out.push(hl); ids.push(hl.id); }
  if (body) { const tt = text(x + w / 2, y, body, { size: S.body, color: SUB }); out.push(tt); ids.push(tt.id); }
  r.customData = { stack: ids, icon, iconColor: DEEP[fill] || INK };
  return out;
}

function frame(x, y, w, h, title) {
  return [base({ id: nid("f"), type: "rectangle", x, y, width: w, height: h, strokeStyle: "dashed", strokeColor: MUTED, roughness: 0, roundness: { type: 3 } }),
    text(x + 20, y + 12, title, { size: S.frame, align: "left", color: SUB })];
}

function arrow(pts, label, { dashed = false, both = false, lx, ly } = {}) {
  const [x0, y0] = pts[0];
  const a = base({ id: nid("a"), type: "arrow", x: x0, y: y0, width: 0, height: 0, points: pts.map(([x, y]) => [x - x0, y - y0]),
    strokeStyle: dashed ? "dashed" : "solid", roundness: pts.length > 2 ? null : { type: 2 }, startBinding: null, endBinding: null,
    startArrowhead: both ? "arrow" : null, endArrowhead: "arrow", lastCommittedPoint: null, elbowed: false });
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  a.width = Math.max(...xs) - Math.min(...xs);
  a.height = Math.max(...ys) - Math.min(...ys);
  const out = [a];
  if (label) {
    const mx = lx ?? (pts[0][0] + pts[pts.length - 1][0]) / 2, my = ly ?? (pts[0][1] + pts[pts.length - 1][1]) / 2 - 22;
    const lt = text(mx, my, label, { size: S.label, color: SUB });
    lt.customData = { cx: mx, cy: my };
    out.push(lt);
  }
  return out;
}

function head(title, sub) {
  const t = text(20, 6, title, { size: S.title, align: "left" });
  t.customData = { titleIcon: true };
  return [t, text(22, 66, sub, { size: S.sub, align: "left", color: SUB })];
}

function save(name, els) {
  writeFileSync(new URL(`./${name}.excalidraw`, import.meta.url), JSON.stringify({ type: "excalidraw", version: 2, source: "strata-local-llm",
    elements: els.flat(), appState: { viewBackgroundColor: "#fffdf7", gridSize: null }, files: {} }, null, 1));
  console.log("wrote", name, els.flat().length);
}

// 1. 시스템 구조 ---------------------------------------------------------------
save("01_architecture", [
  head("시스템 구조", "작은 티켓은 로컬 GPU 로, 검토와 적용은 지휘자가"),
  frame(20, 120, 360, 520, "노트북"),
  box(50, 180, 300, 130, "지휘자", "Claude Code · Codex", { fill: C.violet, icon: "compass" }),
  box(50, 420, 300, 140, "검토 · 적용", "diff 확인 → git apply", { fill: C.gray, icon: "list-checks" }),
  frame(600, 120, 1040, 640, "본체 PC · RTX 5070 Ti 16GB"),
  box(640, 180, 420, 130, "워커 (MCP)", "위임 전 확인 · 실패 넘기기", { fill: C.green, icon: "bot" }),
  box(640, 390, 420, 140, "하네스 H12", "탐색 · 편집 · 검사 루프", { fill: C.yellow, icon: "wrench" }),
  box(640, 620, 420, 110, "작업 사본", "고정 커밋 + pytest", { fill: C.gray, icon: "folder-git-2" }),
  box(1230, 360, 380, 200, "STRATA 서버", "Qwen3.6-35B · E2 엔진\n64K 문맥", { fill: C.blue, icon: "cpu" }),
  arrow([[350, 245], [640, 245]], "MCP 위임", { lx: 495, ly: 215 }),
  arrow([[640, 290], [350, 480]], "diff · 결과", { lx: 470, ly: 330 }),
  arrow([[850, 310], [850, 390]], "티켓", { lx: 900, ly: 350 }),
  arrow([[1060, 430], [1230, 430]], "요청", { lx: 1145, ly: 405 }),
  arrow([[1230, 500], [1060, 500]], "도구 호출", { lx: 1145, ly: 475 }),
  arrow([[850, 530], [850, 620]], "읽기 · 편집 · 테스트", { lx: 990, ly: 575, both: true }),
]);

// 2. 측정 한 회의 데이터 흐름 ----------------------------------------------------
const col = [40, 400, 760, 1120], W = 320, H = 140;
save("02_run_dataflow", [
  head("측정 한 회의 데이터 흐름", "한 행 = 과제 × 회차 × 설정 · 숨은 테스트는 모델에 보이지 않는다"),
  box(col[0], 130, W, H, "1 과제", "고정 커밋 · 숨은 테스트", { fill: C.gray, icon: "clipboard-list" }),
  box(col[1], 130, W, H, "2 작업 사본", "실행마다 새로", { fill: C.gray, icon: "folder-git-2" }),
  box(col[2], 130, W, H, "3 모델 루프", "입력은 prompt 만", { fill: C.yellow, icon: "wrench" }),
  box(col[3], 130, W, H, "4 채점", "숨은 테스트 + 회귀", { fill: C.green, icon: "clipboard-check" }),
  box(col[3], 380, W, H, "5 원장", "1행 추가", { fill: C.blue, icon: "book-open" }),
  box(col[2], 380, W, H, "6 실행 기록", "턴 · 도구 · 답", { fill: C.blue, icon: "scroll-text" }),
  box(col[1], 380, W, H, "7 기록 커밋", "훅이 트레일러 검사", { fill: C.violet, icon: "git-commit-horizontal" }),
  box(col[0], 380, W, H, "8 판정", "30회 짝 비교 → 결정", { fill: C.red, icon: "scale" }),
  arrow([[col[0] + W, 200], [col[1], 200]]),
  arrow([[col[1] + W, 200], [col[2], 200]]),
  arrow([[col[2] + W, 200], [col[3], 200]]),
  arrow([[col[3] + W / 2, 270], [col[3] + W / 2, 380]]),
  arrow([[col[2] + W / 2, 270], [col[2] + W / 2, 380]], "", { dashed: true }),
  arrow([[col[3] + W / 2, 520], [col[3] + W / 2, 580], [col[1] + W / 2 + 40, 580], [col[1] + W / 2 + 40, 520]]),
  arrow([[col[2], 450], [col[1] + W, 450]]),
  arrow([[col[1], 450], [col[0] + W, 450]]),
]);

// 3. 실험 데이터 모델 (ERD 대신) --------------------------------------------------
const L = 40, R = 1220, EW = 320, EH = 120;
save("03_data_model", [
  head("실험 데이터 모델", "한 행 = 과제 × 회차 × 설정 · 원장은 코드만 쓴다(append-only)"),
  box(L, 150, EW, EH, "모델", "sha256", { fill: C.gray, icon: "brain" }),
  box(L, 340, EW, EH, "엔진", "커밋 E0 → E2", { fill: C.gray, icon: "cpu" }),
  box(L, 530, EW, EH, "설정", "하네스 · 문맥 · 샘플링", { fill: C.gray, icon: "sliders-horizontal" }),
  box(540, 190, 500, 420, "원장 한 행", "LEDGER.tsv\n\nrun_id · 결과\n토큰 · 시간\n모델 · 엔진 · 설정 해시", { fill: C.blue, icon: "book-open" }),
  box(R, 150, EW, EH, "과제", "세트 · 유형 · 고정 커밋", { fill: C.yellow, icon: "clipboard-list" }),
  box(R, 340, EW, EH, "실행 기록", "턴 · 도구 · 답", { fill: C.yellow, icon: "scroll-text" }),
  box(R, 530, EW, EH, "결정", "채택 · 보류 · 기각", { fill: C.red, icon: "gavel" }),
  arrow([[540, 260], [L + EW, 210]], "N : 1", { lx: 450, ly: 205 }),
  arrow([[540, 400], [L + EW, 400]], "N : 1", { lx: 450, ly: 375 }),
  arrow([[540, 540], [L + EW, 590]], "N : 1", { lx: 450, ly: 595 }),
  arrow([[1040, 260], [R, 210]], "N : 1", { lx: 1130, ly: 205 }),
  arrow([[1040, 400], [R, 400]], "1 : 1", { lx: 1130, ly: 375 }),
  arrow([[R, 590], [1040, 540]], "N : M", { lx: 1130, ly: 595 }),
]);

// 4. F1 평가 분리 -----------------------------------------------------------------
save("04_f1_separation", [
  head("최종 평가 F1: 출제 · 실행 · 튜닝 분리", "빨간 점선 = 공개하지 않는 것"),
  box(40, 150, 280, 130, "Codex (출제)", "새 저장소 4개 · 30과제", { fill: C.violet, icon: "pencil-ruler" }),
  box(400, 140, 340, 150, "final_eval/", "과제 · 숨은 테스트", { fill: C.gray, dashed: true, stroke: RED, icon: "lock" }),
  box(820, 140, 340, 150, "검증기 V1~V7", "기준 실패 · 참조 통과\n두 번 같은 결과", { fill: C.green, icon: "shield-check" }),
  box(1240, 140, 300, 150, "_validation/", "상세 기록", { fill: C.gray, dashed: true, stroke: RED, icon: "lock" }),
  box(400, 400, 340, 150, "F1 체인", "prompt 만 입력\n30과제 × 3회", { fill: C.yellow, icon: "flask-conical" }),
  box(820, 400, 340, 150, "원장 (공개)", "ID · 통과 · 시간", { fill: C.blue, icon: "book-open" }),
  box(820, 620, 340, 120, "runs/f1_*", "prompt · 패치", { fill: C.gray, dashed: true, stroke: RED, icon: "lock" }),
  box(1240, 410, 300, 150, "Claude Code", "ID · 통과 여부만 본다", { fill: C.violet, icon: "eye-off" }),
  arrow([[320, 215], [400, 215]], "출제", { lx: 360, ly: 180 }),
  arrow([[740, 215], [820, 215]]),
  arrow([[1160, 215], [1240, 215]], "상세", { lx: 1200, ly: 180 }),
  arrow([[570, 290], [570, 400]], "prompt 만", { lx: 650, ly: 345 }),
  arrow([[740, 475], [820, 475]], "채점", { lx: 780, ly: 440 }),
  arrow([[700, 550], [700, 680], [820, 680]], "기록", { lx: 650, ly: 640 }),
  arrow([[1070, 290], [1070, 340], [1390, 340], [1390, 410]], "화면: ID · 통과", { lx: 1230, ly: 312 }),
  arrow([[1160, 485], [1240, 485]], "집계", { lx: 1200, ly: 450 }),
]);
