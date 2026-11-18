`KVStore` 는 표준 라이브러리(`time`, `json`, `typing`, `copy`)만 사용하여 구현됩니다. 트랜잭션 관리는 스택 기반 레이어 스코프 구조로 처리하며, TTL 은 절대 만료 시각으로 내부 관리하고 공개 시에는 남은 시간(초)으로 변환합니다.

```python
import time
import json
import copy
from typing import Any, Optional, Dict, List

_DELETED = object()


class KVStore:
    """인메모리 키-값 저장소입니다. TTL 만료와 중첩 트랜잭션을 지원합니다."""

    def __init__(self, clock=None) -> None:
        self._clock = clock if clock is not None else time.monotonic
        self._committed: Dict[str, Any] = {}  # {key: (value, expiry_time)}
        self._scopes: List[Dict[str, Any]] = [{}]  # 트랜잭션 레이어 스택
        self._sets_count: int = 0
        self._deletes_count: int = 0

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """키에 값을 저장합니다. TTL 이 지정되면 해당 시간 후 키가 자동으로 만료됩니다."""
        if ttl is None:
            expiry = None
        else:
            expiry = self._clock() + ttl

        # 현재 스코프(가장 안쪽 트랜잭션)의 상태를 업데이트합니다.
        # 이전에 이 키에 대한 pending 변경이 있었다면 제거합니다.
        for scope in reversed(self._scopes):
            if key in scope:
                del scope[key]
                break

        self._scopes[-1][key] = (value, expiry)
        self._sets_count += 1

    def get(self, key: str, default=None) -> Any:
        """키에 대응하는 값을 반환합니다. 키가 없거나 만료되었으면 default 를 리턴합니다."""
        # 1. 트랜잭션 스택(안쪽에서 바깥으로) 조회
        for scope in reversed(self._scopes):
            if key in scope:
                val, expiry = scope[key]
                if val is _DELETED or (expiry is not None and self._clock() >= expiry):
                    return default
                return val

        # 2. 커밋된 데이터 조회
        if key in self._committed:
            val, expiry = self._committed[key]
            if val is _DELETED or (expiry is not None and self._clock() >= expiry):
                return default
            return val

        return default

    def delete(self, key: str) -> bool:
        """키를 삭제합니다. 존재하면 True, 아니면 False 를 반환합니다."""
        # 먼저 키가 실제로 살아있는지 확인
        if not self.get(key) and key not in self._get_all_alive_keys():
            return False

        # 현재 스코프에 삭제 플래그 기록
        for scope in reversed(self._scopes):
            if key in scope:
                del scope[key]
                break
        self._scopes[-1][key] = (_DELETED, None)
        self._deletes_count += 1
        return True

    def keys(self, prefix: str = "") -> List[str]:
        """현재 트랜잭션 상태까지 반영된 살아 있는 키를 prefix 조건에 따라 정렬하여 반환합니다."""
        alive_keys = self._get_all_alive_keys()
        if prefix:
            alive_keys = [k for k in alive_keys if k.startswith(prefix)]
        return sorted(alive_keys)

    def _get_all_alive_keys(self) -> List[str]:
        """커밋 상태와 현재 모든 트랜잭션 레이어를 합쳐 살아있는 키 목록을 반환합니다."""
        # 바깥에서 안쪽으로 덮어쓰는 논리 적용
        merged: Dict[str, Any] = {}
        
        # 커밋된 데이터 우선 병합
        for k, v in self._committed.items():
            if v[0] is not _DELETED and (v[1] is None or self._clock() < v[1]):
                merged[k] = v
                
        # 트랜잭션 레이어(안쪽이 우선) 병합
        for scope in reversed(self._scopes):
            for k, v in scope.items():
                if v is _DELETED:
                    merged.pop(k, None)
                else:
                    # pending 값은 만료 시간만 고려하고 실제 커밋 전이라 일단 저장
                    merged[k] = v
                    
        now = self._clock()
        return [k for k, (val, exp) in merged.items() if val is not _DELETED and (exp is None or now < exp)]

    def begin(self) -> None:
        """새로운 트랜잭션을 시작합니다. 중첩 가능합니다."""
        self._scopes.append({})

    def commit(self) -> None:
        """현재 가장 안쪽 트랜잭션을 커밋합니다. 트랜잭션이 없으면 RuntimeError 를 발생시킵니다."""
        if not self._scopes or len(self._scopes) == 1:
            raise RuntimeError("No active transaction to commit.")
            
        pending = self._scopes.pop()
        target = self._scopes[-1] if self._scopes else self._committed
        
        for k, v in pending.items():
            if v is _DELETED:
                target.pop(k, None)
            else:
                target[k] = v

    def rollback(self) -> None:
        """현재 가장 안쪽 트랜잭션을 취소합니다. 트랜잭션이 없으면 RuntimeError 를 발생시킵니다."""
        if not self._scopes or len(self._scopes) == 1:
            raise RuntimeError("No active transaction to rollback.")
            
        self._scopes.pop()

    def snapshot(self) -> str:
        """커밋된 상태의 살아 있는 키와 남은 TTL 을 JSON 문자열로 직렬화하여 반환합니다."""
        alive = self._get_all_alive_keys()
        data = {}
        now = self._clock()
        for k in alive:
            val, exp = self._committed[k]
            remaining_ttl = (exp - now) if exp is not None else None
            data[k] = {"value": val, "remaining_ttl": remaining_ttl}
            
        return json.dumps(data, ensure_ascii=False, default=lambda o: f"<non-serializable: {type(o).__name__}>")

    @classmethod
    def restore(cls, data: str, clock=None) -> "KVStore":
        """JSON 스냅샷 문자열에서 KVStore 인스턴스를 복원합니다."""
        new_store = cls(clock=clock)
        store_data = json.loads(data)
        
        for key, entry in store_data.items():
            val = entry["value"]
            remaining_ttl = entry.get("remaining_ttl")
            if remaining_ttl is not None:
                # 복원 시점의 clock 을 기준으로 TTL 다시 계산
                new_store.set(key, val, max(0.0, remaining_ttl))
            else:
                new_store.set(key, val, None)
                
        return new_store

    def stats(self) -> dict:
        """저장소의 상태를 통계 정보로 반환합니다."""
        return {
            "keys": len(self._get_all_alive_keys()),
            "sets": self._sets_count,
            "deletes": self._deletes_count,
            "depth": len(self._scopes) - 1
        }
```