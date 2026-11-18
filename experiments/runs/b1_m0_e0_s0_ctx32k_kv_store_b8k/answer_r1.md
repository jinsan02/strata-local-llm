이 과제는 트랜잭션 중첩, TTL 만료 처리, 상태 스냅샷/복원 기능을 표준 라이브러리만으로 구현해야 합니다. 핵심 설계는 다음과 같습니다:

1. **저장 구조**: `_data` 딕셔너리에 `key -> {"value": ..., "expires_at": float | None}` 형태로 저장합니다.
2. **트랜잭션**: `begin()` 시 현재 `_data`의 깊은 복사본을 스택에 푸시합니다. 중첩 트랜잭션에서도 가장 안쪽 커밋/롤백이 바깥 상태와 격리되도록 합니다. 롤백 시 복원된 스냅샷으로 `_data` 참조를 교체합니다.
3. **TTL 관리**: `set` 시 기준 시각 + TTL 로 `expires_at` 을 계산합니다. 조회 메서드(`get`, `keys`, `stats`) 는 현재 시각과 비교해 만료된 키는 존재하지 않는 것으로 취급합니다.
4. **스냅샷/복원**: `snapshot()` 은 활성 트랜잭션이 있다면 외곽 상태(스택 최상단) 를 기준으로, 없으면 현재 `_data` 를 기준으로 살아있는 키만 JSON 으로 직렬화합니다. `restore()` 는 남은 TTL 을 복원 시점의 클럭을 기준으로 다시 만료 시각으로 변환해 채웁니다.

```python
import time
import json
import copy
from typing import Any, Dict, List, Optional, Callable


class KVStore:
    """트랜잭션 및 TTL 을 지원하는 키-값 저장소 클래스."""

    def __init__(self, clock: Optional[Callable[[], float]] = None) -> None:
        self._clock = clock or time.monotonic
        # 내부 저장소: key -> {"value": Any, "expires_at": float | None}
        self._data: Dict[str, Dict[str, Any]] = {}
        # 트랜잭션 스택: begin() 시의 _data 스냅샷 기록
        self._tx_stack: List[Dict[str, Dict[str, Any]]] = []
        self._set_count: int = 0
        self._delete_count: int = 0

    def _now(self) -> float:
        """현재 클럭 시각을 반환합니다."""
        return self._clock()

    def _is_expired(self, entry: Optional[Dict[str, Any]]) -> bool:
        """키 엔트리가 만료되었거나 None 인지 판별합니다."""
        if entry is None:
            return True
        if entry["expires_at"] is None:
            return False
        return self._now() >= entry["expires_at"]

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """
        키-값 쌍을 저장합니다.
        ttl 이 지정되면 해당 초수 후 키가 자동으로 만료됩니다.
        동일한 키에 다시 set 하면 기존 TTL 은 새 값으로 덮어씁니다.
        """
        self._set_count += 1
        expires_at = self._now() + ttl if ttl is not None else None
        self._data[key] = {"value": value, "expires_at": expires_at}

    def get(self, key: str, default: Any = None) -> Any:
        """
        키에 매핑된 값을 반환합니다.
        키가 없거나 TTL 만료 시 default 를 반환합니다.
        """
        entry = self._data.get(key)
        if entry is None or self._is_expired(entry):
            return default
        return entry["value"]

    def delete(self, key: str) -> bool:
        """
        키를 물리적으로 삭제합니다.
        살아있는 키가 지워지면 True, 없거나 만료된 키면 False 를 반환합니다.
        """
        entry = self._data.get(key)
        if entry is not None and not self._is_expired(entry):
            del self._data[key]
            self._delete_count += 1
            return True
        return False

    def keys(self, prefix: str = "") -> List[str]:
        """
        현재 저장소에서 살아있는 키 중 주어진 prefix 로 시작하는 키들을
        사전순으로 정렬하여返回列表합니다.
        """
        now = self._now()
        result = []
        for k, v in self._data.items():
            if v["expires_at"] is None or now < v["expires_at"]:
                if k.startswith(prefix):
                    result.append(k)
        return sorted(result)

    def begin(self) -> None:
        """
        새로운 트랜잭션을 시작합니다.
        중첩 호출이 가능하며, 이후 변경사항은 commit 또는 rollback 까지 일시적입니다.
        """
        self._tx_stack.append(copy.deepcopy(self._data))

    def commit(self) -> None:
        """
        가장 안쪽(현재) 트랜잭션의 변경사항을 확정합니다.
        활성 트랜잭션이 없을 경우 RuntimeError 를 발생시킵니다.
        """
        if not self._tx_stack:
            raise RuntimeError("No active transaction to commit.")
        self._tx_stack.pop()

    def rollback(self) -> None:
        """
        가장 안쪽(현재) 트랜잭션의 변경사항을 모두 취소합니다.
        활성 트랜잭션이 없을 경우 RuntimeError 를 발생시킵니다.
        """
        if not self._tx_stack:
            raise RuntimeError("No active transaction to rollback.")
        # 스냅샷 참조를 현재 데이터에 다시 할당하여 이전 상태로 되돌립니다.
        self._data = self._tx_stack.pop()

    def snapshot(self) -> str:
        """
        커밋된 상태(진행 중인 트랜잭션 변경 제외)의 살아있는 키를 JSON 문자열로 반환합니다.
        각 키에는 값과 남은 TTL(초, float | null) 이 포함됩니다.
        """
        base = self._tx_stack[-1] if self._tx_stack else self._data
        now = self._now()
        alive = {}
        for k, v in base.items():
            if v["expires_at"] is None or now < v["expires_at"]:
                remaining = v["expires_at"] - now if v["expires_at"] is not None else None
                alive[k] = {"value": v["value"], "ttl": remaining}
        return json.dumps(alive, ensure_ascii=False)

    @classmethod
    def restore(cls, data: str, clock: Optional[Callable[[], float]] = None) -> 'KVStore':
        """
        snapshot() 이 생성한 JSON 문자열을 읽어 새 KVStore 인스턴스를 복원합니다.
        남은 TTL 은 복원 시점의 clock 기준으로 다시 계산됩니다.
        """
        obj = cls(clock=clock or time.monotonic)
        payload = json.loads(data)
        now = obj._now()
        for k, v in payload.items():
            ttl = v.get("ttl")
            expires_at = (now + ttl) if ttl is not None else None
            obj._data[k] = {"value": v["value"], "expires_at": expires_at}
        return obj

    def stats(self) -> Dict[str, Any]:
        """
        현재 저장소의 상태 통계를 반환합니다.
        - keys: 커밋된 상태의 살아있는 키 수
        - sets: set() 호출 총 횟수
        - deletes: 성공적으로 삭제된 delete() 횟수
        - depth: 현재 활성화된 트랜잭션 중첩 깊이
        """
        now = self._now()
        # 커밋된 상태의 살아있는 키 수 계산
        base = self._tx_stack[-1] if self._tx_stack else self._data
        alive_keys = sum(
            1 for v in base.values()
            if v["expires_at"] is None or now < v["expires_at"]
        )
        return {
            "keys": alive_keys,
            "sets": self._set_count,
            "deletes": self._delete_count,
            "depth": len(self._tx_stack)
        }
```