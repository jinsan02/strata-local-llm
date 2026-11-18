이 구현은 표준 라이브러리(`time`, `json`)만 사용하며, 트랜잭션 격리 및 TTL 만료를 효율적으로 처리합니다. 핵심 설계는 다음과 같습니다.

- **데이터 구조**: 커밋된 상태는 `_data` 딕셔너리, 트랜잭션 변경사항은 스택(`_txn_stack`)의 레이어로 관리합니다. 각 레이어는 키를 매핑하고 `None`은 삭제(Tombstone)를 의미합니다.
- **조회(`get`, `keys`)**: 현재 레이어에서 아래쪽으로 탐색하여 가장 최근 변경사항을 우선 적용합니다. TTL 만료 시점(절대 시각)을 저장하므로 접근 시점에 실시간으로 만료 여부를 판정합니다.
- **트랜잭션 병합(`commit`)**: 최상위 레이어의 변경사항을 `_data`에 일괄 반영하고 제거한 후 스택에서 팝합니다. 중첩된 트랜잭션도 동일하게 동작합니다.
- **스냅샷/복원**: JSON 직렬화 시 절대 만료 시각(`exp`)을 저장합니다. `restore` 시 새 `clock` 기준으로 `_now()`를 사용하면 남은 TTL이 자동으로 재계산됩니다.

```python
import time
import json
from typing import Any, Callable, Dict, List, Optional


class KVStore:
    """메모리 기반 키-값 저장소로 TTL 및 중첩 트랜잭션을 지원합니다."""

    def __init__(self, clock: Optional[Callable[[], float]] = None) -> None:
        self._clock = clock if clock is not None else time.monotonic
        # 커밋된 상태: key -> (value, absolute_expiry_time | None)
        self._data: Dict[str, tuple[Any, Optional[float]]] = {}
        # 트랜잭션 스택: 각 레이어는 key -> (value, expiry) | None (None은 삭제 표시)
        self._txn_stack: List[Dict[str, Optional[tuple[Any, Optional[float]]]]] = []
        self._set_count: int = 0
        self._del_count: int = 0

    def _now(self) -> float:
        return self._clock()

    def _is_expired(self, rec: Optional[tuple], now: float) -> bool:
        if rec is None:
            return True
        expiry = rec[1]
        return expiry is not None and now >= expiry

    def _get_record(self, key: str) -> Optional[tuple[Any, Optional[float]]]:
        """현재 트랜잭션 컨텍스트에서 키의 레코드 또는 None을 반환합니다."""
        for layer in reversed(self._txn_stack):
            if key in layer:
                rec = layer[key]
                # None은 트랜잭션 내 삭제(Tombstone)를 의미
                return None if rec is None else rec
        return self._data.get(key)

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """값을 저장합니다. TTL이 경과하면 키가 만료됩니다."""
        now = self._now()
        expiry = now + ttl if ttl is not None else None
        rec = (value, expiry)
        self._set_count += 1

        if self._txn_stack:
            self._txn_stack[-1][key] = rec
        else:
            self._data[key] = rec

    def get(self, key: str, default: Any = None) -> Any:
        """현재 유효한 값을 조회합니다. 없거나 만료된 경우 default를 반환합니다."""
        now = self._now()
        rec = self._get_record(key)
        if rec is None or self._is_expired(rec, now):
            return default
        return rec[0]

    def delete(self, key: str) -> bool:
        """키를 삭제합니다. 존재하고 만료되지 않은 경우에만 성공하여 True를 반환합니다."""
        rec = self._get_record(key)
        now = self._now()
        if rec is None or self._is_expired(rec, now):
            return False

        self._del_count += 1
        if self._txn_stack:
            # 트랜잭션 내에서 삭제를 표현하기 위해 Tombstone 사용
            self._txn_stack[-1][key] = None
        else:
            del self._data[key]
        return True

    def keys(self, prefix: str = "") -> List[str]:
        """현재 유효한 키 중 prefix로 시작하는 것을 사전순으로 반환합니다."""
        now = self._now()
        candidates = set(self._data.keys())
        for layer in self._txn_stack:
            candidates.update(layer.keys())

        live_keys = []
        for k in candidates:
            rec = self._get_record(k)
            if rec is not None and not self._is_expired(rec, now):
                if k.startswith(prefix):
                    live_keys.append(k)
        return sorted(live_keys)

    def begin(self) -> None:
        """새로운 트랜잭션을 시작합니다. 중첩 가능합니다."""
        self._txn_stack.append({})

    def commit(self) -> None:
        """현재 활성 트랜잭션의 변경사항을 저장소에 반영합니다."""
        if not self._txn_stack:
            raise RuntimeError("No active transaction to commit.")
        
        layer = self._txn_stack.pop()
        for key, rec in layer.items():
            if rec is None:
                # 트랜잭션에서 삭제를 표시한 키는 커밋 시 실제 제거
                self._data.pop(key, None)
            else:
                self._data[key] = rec

    def rollback(self) -> None:
        """현재 활성 트랜잭션의 변경사항을 취소합니다."""
        if not self._txn_stack:
            raise RuntimeError("No active transaction to rollback.")
        
        self._txn_stack.pop()

    def snapshot(self) -> str:
        """커밋된 상태의 살아있는 키와 남은 TTL 정보를 JSON 문자열로 반환합니다."""
        now = self._now()
        live_data = {}
        for k, rec in self._data.items():
            if not self._is_expired(rec, now):
                # value는 JSON 직렬화 가능하다고 가정하고 그대로 저장
                live_data[k] = {"v": rec[0], "exp": rec[1]}
        return json.dumps(live_data)

    @classmethod
    def restore(cls, data: str, clock: Optional[Callable[[], float]] = None) -> "KVStore":
        """스냅샷 JSON에서 새 KVStore 인스턴스를 복원합니다."""
        store = cls(clock=clock)
        live_data = json.loads(data)
        for k, info in live_data.items():
            # exp는 절대 시각이므로, 새로 할당된 clock의 _now() 기준으로 
            # TTL 만료 판정이 자동으로 재계산됩니다.
            store._data[k] = (info["v"], info["exp"])
        return store

    def stats(self) -> Dict[str, Any]:
        """저장소의 상태 통계(dict)를 반환합니다."""
        now = self._now()
        live_committed = sum(1 for rec in self._data.values() if not self._is_expired(rec, now))
        return {
            "keys": live_committed,
            "sets": self._set_count,
            "deletes": self._del_count,
            "depth": len(self._txn_stack)
        }
```