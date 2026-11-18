# 설계 개요
- **저장 구조**: 커밋된 데이터는 `dict[str, (value, expire_time)]`로 관리하며 TTL 만료 시각을 절대값으로 저장합니다.
- **트랜잭션**: 스택(`list[dict]`)으로 중첩 상태를 추적합니다. 각 레벨은 `{key: (op_type, value, expire)}` 형태를 가지며, `commit` 시 상단 변경사항만 커밋 데이터에 병합하고, `rollback` 시 해당 레벨을 버립니다.
- **조회 일관성**: `get`, `keys`는 트랜잭션 스택을 하위→상위 순서로 스캔한 후 커밋 데이터에서 TTL 만료 여부를 체크합니다.
- **TTL 관리**: 실제 데이터 정리(Lazy Eviction) 없이 조회 시점에 만료를 판정하며, `snapshot`과 `restore`에서는 남은 TTL을 새 기준 시각에 맞게 재계산합니다.

```python
import time
import json
from typing import Any, Optional

class KVStore:
    """메모리 기반 키-값 저장소 (TTL 및 중첩 트랜잭션 지원)"""

    def __init__(self, clock: Optional[Any] = None) -> None:
        """생성자. clock은 인자 없이 현재 시간(float)을 돌려주는 함수입니다."""
        self._clock = clock or time.monotonic
        self._data: dict[str, tuple[Any, Optional[float]]] = {}
        self._txn_stack: list[dict[str, tuple[str, Any, Optional[float]]]] = []
        self._sets_count: int = 0
        self._deletes_count: int = 0

    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """값을 저장합니다. ttl이 지정되면 해당 시간(초) 후 만료됩니다."""
        self._sets_count += 1
        now = self._clock()
        expire = now + ttl if ttl is not None else None

        if self._txn_stack:
            self._txn_stack[-1][key] = ('SET', value, expire)
        else:
            self._data[key] = (value, expire)

    def get(self, key: str, default: Any = None) -> Any:
        """값을 반환하거나 키가 없으면 default를 돌려줍니다."""
        for txn in reversed(self._txn_stack):
            if key in txn:
                op, val, _ = txn[key]
                return default if op == 'DEL' else val

        if key in self._data:
            val, exp = self._data[key]
            if exp is not None and self._clock() >= exp:
                return default
            return val
        return default

    def delete(self, key: str) -> bool:
        """키를 삭제합니다. 존재하고 성공적으로 지웠으면 True, 아니면 False."""
        for txn in reversed(self._txn_stack):
            if key in txn:
                op, _, _ = txn[key]
                if op == 'DEL':
                    return False
                self._deletes_count += 1
                self._txn_stack[-1][key] = ('DEL', None, None)
                return True

        if key in self._data:
            val, exp = self._data[key]
            if exp is not None and self._clock() >= exp:
                return False
            self._deletes_count += 1
            if self._txn_stack:
                self._txn_stack[-1][key] = ('DEL', None, None)
            else:
                del self._data[key]
            return True
        return False

    def keys(self, prefix: str = "") -> list[str]:
        """TTL이 지나지 않은 키 중 prefix로 시작하는 것을 사전순으로 반환합니다."""
        alive_keys = set()
        for txn in self._txn_stack:
            for k, (op, _, _) in txn.items():
                if op == 'SET': alive_keys.add(k)
                elif op == 'DEL': alive_keys.discard(k)

        now = self._clock()
        for k, (_, exp) in self._data.items():
            if exp is None or now < exp:
                alive_keys.add(k)

        return sorted(k for k in alive_keys if k.startswith(prefix))

    def begin(self) -> None:
        """트랜잭션을 시작합니다. 중첩 가능합니다."""
        self._txn_stack.append({})

    def commit(self) -> None:
        """가장 안쪽 트랜잭션의 변경을 커밋합니다."""
        if not self._txn_stack:
            raise RuntimeError("No active transaction to commit")
        changes = self._txn_stack.pop()
        for k, (op, val, exp) in changes.items():
            if op == 'SET':
                self._data[k] = (val, exp)
            elif op == 'DEL':
                self._data.pop(k, None)

    def rollback(self) -> None:
        """가장 안쪽 트랜잭션의 변경을 버립니다."""
        if not self._txn_stack:
            raise RuntimeError("No active transaction to rollback")
        self._txn_stack.pop()

    def snapshot(self) -> str:
        """커밋된 상태의 살아있는 키와 남은 TTL을 JSON 문자열로 반환합니다."""
        now = self._clock()
        result = {}
        for k, (v, exp) in self._data.items():
            if exp is None or now < exp:
                ttl_rem = round(exp - now, 2) if exp is not None else None
                result[k] = {"v": v, "ttl_rem": ttl_rem}
        return json.dumps(result, ensure_ascii=False)

    @classmethod
    def restore(cls, data: str, clock: Optional[Any] = None) -> 'KVStore':
        """snapshot 결과에서 새 저장소를 복원합니다."""
        obj = cls(clock=clock)
        parsed = json.loads(data)
        now = obj._clock()
        for k, info in parsed.items():
            v = info["v"]
            ttl_rem = info.get("ttl_rem")
            expire = now + ttl_rem if ttl_rem is not None else None
            obj._data[k] = (v, expire)
        return obj

    def stats(self) -> dict:
        """저장소의 통계 정보({keys, sets, deletes, depth})를 반환합니다."""
        now = self._clock()
        alive_committed = sum(1 for _, (_, exp) in self._data.items() if exp is None or now < exp)
        return {
            "keys": alive_committed,
            "sets": self._sets_count,
            "deletes": self._deletes_count,
            "depth": len(self._txn_stack)
        }
```