# 구현 개요
* **저장 구조**: 커밋된 상태(`_store`)와 트랜잭션 스택(`_stack`, `_del_stack`)을 분리합니다. 각 트랜잭션 레벨은 시작 시점의 데이터 복사본과 해당 레벨에서만 발생한 삭제 키 집합을 유지합니다.
* **TTL 관리**: 만료 시각(`exp`)은 절대 시간으로 저장합니다. 조회/삭제 시 현재 시각과 비교하여 유효성 판단하며, expired된 키는 즉시 제거하지 않고 지연 정거(Lazy expiration)로 처리합니다.
* **트랜잭션 격리 및 병합**: `begin()` 시 현재 상태를 복사하고 스택에 푸시합니다. `commit()` 시 안쪽 트랜잭션의 변경사항과 삭제 집합을 바깥 레벨(또는 `_store`)에 정합하게 병합합니다.
* **통계/스냅샷**: 통계는 호출 횟수를 직접 카운팅하며, 스냅샷은 커밋된 `_store` 기준 살아있는 키와 남은 TTL을 JSON 직렬화합니다.

# 최종 코드
```python
import time
import json
from typing import Any, Dict, List, Optional, Callable


class KVStore:
    """단일 파일 모듈의 메모리 키-값 저장소 클래스."""

    def __init__(self, clock: Optional[Callable[[], float]] = None) -> None:
        self._clock = clock or time.monotonic
        self._store: Dict[str, dict] = {}  # key -> {"v": Any, "exp": float | None}
        self._stack: List[Dict[str, dict]] = []
        self._del_stack: List[set] = []
        self._curr = self._store
        self._sets = 0
        self._deletes = 0

    def _now(self) -> float:
        return self._clock()

    def _is_alive(self, key: str) -> bool:
        if key not in self._curr:
            return False
        exp = self._curr[key]["exp"]
        return exp is None or self._now() < exp

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """키에 값을 저장합니다. TTL이 지정되면 해당 시간 후 만료됩니다."""
        now = self._now()
        exp = (now + ttl) if ttl is not None else None
        self._curr[key] = {"v": value, "exp": exp}
        self._sets += 1

    def get(self, key: str, default: Any = None) -> Any:
        """존재하고 만료되지 않은 키의 값을 반환합니다. 없으면 default를 줍니다."""
        if self._is_alive(key):
            return self._curr[key]["v"]
        return default

    def delete(self, key: str) -> bool:
        """만료되지 않은 키를 삭제합니다. 성공 시 True, 실패 시 False."""
        now = self._now()
        if key in self._curr:
            exp = self._curr[key]["exp"]
            if exp is None or now < exp:
                del self._curr[key]
                self._del_stack[-1].add(key)
                self._deletes += 1
                return True
        return False

    def keys(self, prefix: str = "") -> List[str]:
        """현재 트랜잭션 뷰에서 prefix로 시작하며 살아있는 키를 사전순으로 반환합니다."""
        now = self._now()
        result = []
        for k, v in self._curr.items():
            if k.startswith(prefix):
                exp = v["exp"]
                if exp is None or now < exp:
                    result.append(k)
        return sorted(result)

    def begin(self) -> None:
        """트랜잭션을 시작합니다. 중첩이 가능합니다."""
        self._stack.append({k: {"v": v["v"], "exp": v["exp"]} for k, v in self._curr.items()})
        self._del_stack.append(set())
        self._curr = self._stack[-1]

    def commit(self) -> None:
        """가장 안쪽 트랜잭션의 변경을 바깥(또는 저장소)에 반영합니다."""
        if not self._stack:
            raise RuntimeError("No active transaction to commit.")
        popped_data = self._stack.pop()
        popped_dels = self._del_stack.pop()

        if self._stack:
            outer = self._stack[-1]
            for k in popped_dels:
                outer.pop(k, None)
            for k, v in popped_data.items():
                outer[k] = v  # TTL은 절대시간이므로 외부에서도 유효성 판단 기준 동일
            self._curr = outer
        else:
            self._store.clear()
            self._store.update(popped_data)
            self._curr = self._store

    def rollback(self) -> None:
        """가장 안쪽 트랜잭션의 변경을 버립니다."""
        if not self._stack:
            raise RuntimeError("No active transaction to rollback.")
        self._stack.pop()
        self._del_stack.pop()
        if self._stack:
            self._curr = self._stack[-1]
        else:
            self._curr = self._store

    def snapshot(self) -> str:
        """커밋된 상태의 살아있는 키와 남은 TTL을 JSON 문자열로 반환합니다."""
        now = self._now()
        alive_keys = {}
        for k, v in self._store.items():
            exp = v["exp"]
            if exp is None or now < exp:
                rem_ttl = None if exp is None else round(max(0.0, exp - now), 6)
                alive_keys[k] = {"value": v["v"], "remaining_ttl": rem_ttl}
        return json.dumps(alive_keys, default=str)

    @classmethod
    def restore(cls, data: str, clock: Optional[Callable[[], float]] = None) -> 'KVStore':
        """스냅샷에서 새 KVStore를 복원합니다. TTL은 복원 시점 기준 재계산됩니다."""
        now = (clock or time.monotonic)()
        store_data = json.loads(data)
        new_store = {}
        for k, v in store_data.items():
            if "remaining_ttl" in v and v["remaining_ttl"] is not None:
                ttl = v["remaining_ttl"]
                exp = now + ttl
            else:
                exp = None
            new_store[k] = {"v": v["value"], "exp": exp}

        inst = cls(clock=clock)
        inst._store = new_store
        inst._curr = inst._store
        return inst

    def stats(self) -> dict:
        """현재 저장소의 통계를 반환합니다."""
        now = self._now()
        alive_count = sum(1 for v in self._store.values() if v["exp"] is None or now < v["exp"])
        return {
            "keys": alive_count,
            "sets": self._sets,
            "deletes": self._deletes,
            "depth": len(self._stack)
        }
```