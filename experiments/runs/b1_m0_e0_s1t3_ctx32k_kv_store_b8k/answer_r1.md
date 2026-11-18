파이썬 표준 라이브러리만으로 구현한 `KVStore` 클래스입니다. 트랜잭션 격리, TTL 만료 처리, 스냅샷/복원, 통계 수집을 모두 포함하며 타입 힌트와 docstring이 명시되어 있습니다.

### 핵심 설계 요약
- **데이터 분리**: 커밋된 상태(`_data`)와 트랜잭션 내 변경사항(`_txn_stack`)을 분리하여 `snapshot()`이 커밋되지 않은 변경을 보지 않도록 합니다.
- **TTL 관리**: 접근 시 지체 만료를 검사하고, 만료되면 `_data`에서 즉시 제거합니다. 중첩 트랜잭션에서도 내부에서 TTL을 우선 적용합니다.
- **스냅샷/복원**: 남은 TTL을 직렬화하여 저장하며, `restore()`는 새 `clock` 기준으로 TTL을 재계산합니다.
- **통계**: 매 `set` 호출과 성공한 `delete`를 별도 카운터로 추적합니다.

```python
import time
import json
from typing import Any, Optional


class KVStore:
    """단일 스레드용 메모리 키-값 저장소 (TTL & 트랜잭션 지원)"""

    def __init__(self, clock: Optional[callable] = None) -> None:
        """저장소를 초기화합니다.

        Args:
            clock: 현재 시각(초 단위 float)을 반환하는 callable. 기본값은 time.monotonic.
        """
        self._clock = clock or time.monotonic
        # 커밋된 실제 데이터: {key: {"value": Any, "set_time": float, "ttl": float | None}}
        self._data: dict[str, dict] = {}
        # 트랜잭션 스택: 각 레벨은 변경된 키의 새로운 상태 또는 None(삭제)를 저장
        self._txn_stack: list[dict[str, Optional[dict]]] = []
        
        # 통계 카운터
        self._sets_count: int = 0
        self._deletes_count: int = 0

    def _is_expired(self, entry: dict) -> bool:
        """엔트리가 TTL 만료되었는지 검사합니다."""
        if entry["ttl"] is None:
            return False
        return self._clock() >= entry["set_time"] + entry["ttl"]

    def _resolve_entry(self, key: str) -> Optional[dict]:
        """키의 현재 유효한 엔트리를 확인합니다. 트랜잭션 우선, 만료 시 제거 후 반환."""
        # 1. 트랜잭션 스택에서 가장 안쪽부터 확인
        for txn in reversed(self._txn_stack):
            if key in txn:
                entry = txn[key]
                if entry is None:
                    return None  # 트랜잭션에서 삭제됨
                if self._is_expired(entry):
                    del txn[key]  # 만료되면 트랜잭션에서도 제거
                    continue
                return entry

        # 2. 커밋된 데이터 확인
        if key in self._data:
            entry = self._data[key]
            if self._is_expired(entry):
                del self._data[key]
                return None
            return entry

        return None

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """키에 값을 저장합니다. TTL이 지정되면 만료 시간이 설정됩니다."""
        now = self._clock()
        self._sets_count += 1
        
        new_entry = {"value": value, "set_time": now, "ttl": ttl}

        if self._txn_stack:
            # 트랜잭션 내부: pending dict에 저장
            self._txn_stack[-1][key] = new_entry
        else:
            # 커밋된 영역에 직접 저장 (트랜잭션 중이 아님)
            self._data[key] = new_entry

    def get(self, key: str, default: Any = None) -> Any:
        """키에 해당하는 값을 반환합니다. 키가 없거나 만료되면 default를 반환합니다."""
        entry = self._resolve_entry(key)
        return entry["value"] if entry is not None else default

    def delete(self, key: str) -> bool:
        """키를 삭제합니다. 존재하고 만료되지 않았으면 True, 아니면 False."""
        resolved = self._resolve_entry(key)
        
        # 트랜잭션 내에서는 삭제 요청을 pending에 기록
        if self._txn_stack:
            self._txn_stack[-1][key] = None
            return resolved is not None  # 실제로 유효한 키였는지 여부에 따라 반환
            
        # 커밋된 영역에서 삭제
        if resolved is not None:
            del self._data[key]
            self._deletes_count += 1
            return True
        return False

    def keys(self, prefix: str = "") -> list[str]:
        """prefix로 시작하는 살아있는 커밋된 키를 사전순으로 반환합니다."""
        # 트랜잭션 내에서도 실제 접근 시 만료 검사 및 pending 상태 고려 필요
        # 요구사항에 따라 '살아 있는 키'는 TTL 만료를 체크해야 하므로 _resolve_entry 활용
        alive = []
        for key in list(self._data.keys()):
            if key.startswith(prefix):
                entry = self._resolve_entry(key)  # 만료 검사 및 pending 확인
                if entry is not None:
                    alive.append(key)
        return sorted(alive)

    def begin(self) -> None:
        """트랜잭션을 시작합니다. 중첩 가능합니다."""
        self._txn_stack.append({})

    def commit(self) -> None:
        """가장 안쪽 트랜잭션의 변경을 커밋(반영)합니다."""
        if not self._txn_stack:
            raise RuntimeError("활성화된 트랜잭션이 없습니다. commit()은 begin() 이후 호출해야 합니다.")
        
        pending = self._txn_stack.pop()
        for key, entry in pending.items():
            if entry is None:
                self._data.pop(key, None)  # 삭제 반영
            else:
                self._data[key] = entry

    def rollback(self) -> None:
        """가장 안쪽 트랜잭션의 변경을 취소합니다."""
        if not self._txn_stack:
            raise RuntimeError("활성화된 트랜잭션이 없습니다. rollback()은 begin() 이후 호출해야 합니다.")
        
        # pending 스택만 버리면 되므로 커밋과 동일한 흐름으로 처리 가능
        self._txn_stack.pop()

    def snapshot(self) -> str:
        """커밋된 상태의 살아있는 키와 남은 TTL을 JSON 문자열로 반환합니다."""
        payload = {}
        for key, entry in list(self._data.items()):
            if not self._is_expired(entry):
                remaining = max(0.0, entry["ttl"] - (self._clock() - entry["set_time"])) if entry["ttl"] is not None else 0.0
                payload[key] = {"value": entry["value"], "remaining_ttl": round(remaining, 6)}
        return json.dumps(payload, sort_keys=True)

    @classmethod
    def restore(cls, data: str, clock: Optional[callable] = None) -> "KVStore":
        """스냅샷 문자열에서 새 KVStore 인스턴스를 복원합니다.

        Args:
            data: snapshot()에서 생성된 JSON 문자열.
            clock: 새 저장소에서 사용할 시간 함수.
        """
        new_store = cls(clock=clock)
        payload = json.loads(data)
        now = new_store._clock()
        
        for key, info in payload.items():
            # 남은 TTL을 기준으로 현재 시각에서 시작하는 엔트리 생성
            ttl_val = info.get("remaining_ttl", 0.0)
            if ttl_val is not None and ttl_val > 0:
                new_entry = {
                    "value": info["value"],
                    "set_time": now,
                    "ttl": ttl_val
                }
            else:
                # TTL이 없거나 0이면 무한대로 처리 (원래 설정 그대로 유지하려면 None 저장)
                # 복원 시점이 이미 만료되었을 수 있으므로 실제 유효성 검사는 접근 시 재계산됨
                new_entry = {
                    "value": info["value"],
                    "set_time": now,
                    "ttl": ttl_val if (ttl_val is not None and ttl_val > 0) else None
                }
            new_store._data[key] = new_entry
        return new_store

    def stats(self) -> dict:
        """저장소의 통계 정보를 반환합니다."""
        # 살아있는 커밋된 키 수 계산 (트랜잭션 영향 받지 않는 순수 _data 기준 + 만료 제거)
        alive_committed = sum(1 for entry in list(self._data.values()) if not self._is_expired(entry))
        return {
            "keys": alive_committed,
            "sets": self._sets_count,
            "deletes": self._deletes_count,
            "depth": len(self._txn_stack)
        }
```