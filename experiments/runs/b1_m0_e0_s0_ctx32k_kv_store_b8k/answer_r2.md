# 구현 개요

* **내부 구조**: 커밋된 데이터는 `_store` 딕셔너리에 저장합니다. 각 키의 값은 `{"op": "s"|"d", "val": ..., "st": float, "ttl": float|None}` 형태로 관리합니다. (`"d"`는 삭제 마커)
* **트랜잭션**: 스택(`_tx_stack`)에 프레임(딕셔너리)을 쌓아 중첩을 지원합니다. `get`/`keys`는 스택 최상위부터 `_store`까지 순차적으로 확인해 가장 안쪽 변경사항이 겹쳐진 상태를 반환합니다.
* **TTL 만료**: 저장 시각(`st`) + `ttl`과 현재 `clock()`을 비교하여 생사를 판단합니다. `set` 재호출 시 기존 엔트리가 완전히 덮어씌워져 TTL도 함께 갱신됩니다.
* **스냅샷/복원**: 커밋된 상태만 JSON으로 직렬화합니다. 복원 시 남은 TTL을 기준으로 새 저장소 시각(`clock()`)부터 다시 타이머를 재시작합니다.
* **통계**: `stats()`는 오직 `_store`에 기반한 살아있는 키 수와 호출 카운트를 반환하며, 진행 중인 트랜잭션의 일시적 변경은 커밋된 상태 통계에는 반영되지 않습니다.

```python
from __future__ import annotations
import time
import json
from typing import Any, Callable, Dict, List, Optional

class KVStore:
    """단일 파일 기반의 TTL 지원 키-값 저장소 클래스 (트랜잭션 중첩 지원)"""

    def __init__(self, clock: Optional[Callable[[], float]] = None) -> None:
        self._clock = clock or time.monotonic
        self._store: Dict[str, Dict[str, Any]] = {}
        self._tx_stack: List[Dict[str, Dict[str, Any]]] = []
        self._stats: Dict[str, int] = {"sets": 0, "deletes": 0}

    def _get_entry(self, key: str) -> Optional[Dict[str, Any]]:
        """현재 스코프에서 키의 실제 데이터를 반환 (트랜잭션 오버레이 반영)"""
        for frame in reversed(self._tx_stack):
            if key in frame:
                return frame[key]
        return self._store.get(key)

    def _is_live(self, entry: Optional[Dict[str, Any]]) -> bool:
        """엔트리가 유효하고 TTL이 만료되지 않았는지 확인"""
        if entry is None or entry.get("op") == "d":
            return False
        st = entry["st"]
        ttl = entry.get("ttl")
        if ttl is None:
            return True
        return self._clock() < st + ttl

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """값을 저장합니다. TTL이 지나면 자동으로 만료되며, 재설정 시 이전 TTL이 초기화됩니다."""
        self._stats["sets"] += 1
        entry = {"op": "s", "val": value, "st": self._clock(), "ttl": ttl}
        
        if not self._tx_stack:
            self._store[key] = entry
        else:
            self._tx_stack[-1][key] = entry

    def get(self, key: str, default: Any = None) -> Any:
        """현재 유효한 값을 반환합니다. 없거나 만료되었으면 default를 반환합니다."""
        entry = self._get_entry(key)
        return entry["val"] if self._is_live(entry) else default

    def delete(self, key: str) -> bool:
        """키를 삭제합니다. 존재하고 유효하면 True, 아니면 False를 반환합니다."""
        entry = self._get_entry(key)
        if not self._is_live(entry):
            return False

        del_entry = {"op": "d"}
        if not self._tx_stack:
            self._store[key] = del_entry
        else:
            self._tx_stack[-1][key] = del_entry
            
        self._stats["deletes"] += 1
        return True

    def keys(self, prefix: str = "") -> List[str]:
        """현재 스코프(트랜잭션 반영 포함)에서 살아있는 키 중 접두사와 일치하는 것을 정렬하여 반환합니다."""
        now = self._clock()
        candidates = set(self._store.keys())
        for frame in self._tx_stack:
            candidates.update(frame.keys())

        result = []
        for key in candidates:
            entry = self._get_entry(key)
            if self._is_live(entry) and key.startswith(prefix):
                result.append(key)
        return sorted(result)

    def begin(self) -> None:
        """트랜잭션을 시작합니다. (중첩 지원)"""
        self._tx_stack.append({})

    def commit(self) -> None:
        """가장 안쪽 트랜잭션의 변경을 바깥 레이어(또는 저장소)에 반영합니다."""
        if not self._tx_stack:
            raise RuntimeError("Commit failed: No active transaction.")
        
        top = self._tx_stack.pop()
        target = self._tx_stack[-1] if len(self._tx_stack) > 0 else self._store
        target.update(top)

    def rollback(self) -> None:
        """가장 안쪽 트랜잭션의 변경을 취소하고 팝합니다."""
        if not self._tx_stack:
            raise RuntimeError("Rollback failed: No active transaction.")
        
        self._tx_stack.pop()

    def snapshot(self) -> str:
        """커밋된 상태의 살아있는 키와 남은 TTL을 JSON 문자열로 직렬화합니다."""
        now = self._clock()
        live_data = {}
        for key, entry in self._store.items():
            if entry["op"] != "s":
                continue
            ttl = entry.get("ttl")
            expires_at = entry["st"] + ttl if ttl is not None else float("inf")
            
            if now < expires_at:
                remaining = max(0.0, expires_at - now) if ttl is not None else 0.0
                live_data[key] = {"value": entry["val"], "remaining_ttl": remaining}
                
        return json.dumps(live_data)

    @classmethod
    def restore(cls, data: str, clock: Optional[Callable[[], float]] = None) -> KVStore:
        """스냅샷 JSON에서 새 저장소를 생성합니다. TTL은 복원 시점의 clock 기준으로 재계산됩니다."""
        parsed = json.loads(data)
        store = cls(clock)
        now = store._clock()
        
        for key, info in parsed.items():
            remaining = info["remaining_ttl"]
            # 남은 TTL이 양수면 유한 TTL로 복원, 아니면 무한 TTL 처리
            new_ttl = remaining if remaining > 0 else None
            new_st = now - remaining if new_ttl is not None else now
            store._store[key] = {"op": "s", "val": info["value"], "st": new_st, "ttl": new_ttl}
            
        return store

    def stats(self) -> Dict[str, Any]:
        """커밋된 상태의 살아있는 키 수, set/delete 호출 횟수, 트랜잭션 깊이를 반환합니다."""
        now = self._clock()
        live_count = 0
        for entry in self._store.values():
            if entry["op"] == "s" and (entry.get("ttl") is None or now < entry["st"] + entry["ttl"]):
                live_count += 1
                
        return {
            "keys": live_count,
            "sets": self._stats["sets"],
            "deletes": self._stats["deletes"],
            "depth": len(self._tx_stack)
        }
```