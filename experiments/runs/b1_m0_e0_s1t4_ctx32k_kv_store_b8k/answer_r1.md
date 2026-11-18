`KVStore` 클래스는 표준 라이브러리(`time`, `json`)만을 사용하여 단일 파일로 구성됩니다. 내부 상태 관리는 커밋되지 않은 데이터를 분리하는 `dict` 기반의 레이어 스택 방식을 채택했으며, TTL 만료는 접근 시점(Base/Transaction 프레임 상위부터 하위까지)에 검산하는 지연 소거(Lazy Expiration) 방식으로 처리합니다. 트랜잭션 커밋 시 변경 사항을 최하단 데이터로 병합하고, 하위 중첩 트랜잭션의 오버레이 키를 정리하여 일관성을 유지합니다.

```python
import time
import json
from typing import Any, Optional


class KVStore:
    """트랜잭션과 TTL을 지원하는 인메모리 키-값 저장소입니다."""

    # 내부 삭제 마커 (None 값과 구분하기 위함)
    _DELETED = object()

    def __init__(self, clock=None):
        """
        Args:
            clock: 현재 시각(초 단위 float)을 반환하는 호출 가능한 객체.
                   지정되지 않으면 time.monotonic() 사용.
        """
        self._clock = clock or time.monotonic
        # base 데이터: {key: {"v": value, "e": expire_at}}
        self._store: dict[str, dict[str, Any]] = {}
        # 트랜잭션 프레임 스택: 각 프레임은 {key: {"v", "e", "del"}}
        self._tx_stack: list[dict[str, dict[str, Any]]] = []
        self._set_count: int = 0
        self._delete_count: int = 0

    def _now(self) -> float:
        return self._clock()

    def _is_expired(self, expire_at: Optional[float]) -> bool:
        return expire_at is not None and self._now() >= expire_at

    def _resolve_value(self, key: str) -> tuple[Any | None, bool]:
        """
        키의 현재 유효 값을 찾습니다.
        반환값: (value, is_live)
        트랜잭션 프레임이 존재할 경우 상위(안쪽)부터 검사합니다.
        """
        # 트랜잭션 프레임 역순 탐색 (가장 안쪽 TX 우선)
        for frame in reversed(self._tx_stack):
            if key in frame:
                entry = frame[key]
                if entry["del"] or self._is_expired(entry.get("e")):
                    return None, False
                return entry["v"], True

        # Base 데이터 검사
        base_entry = self._store.get(key)
        if base_entry is None:
            return None, False
        if self._is_expired(base_entry.get("e")):
            return None, False
        return base_entry["v"], True

    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """키에 값을 저장합니다. TTL이 지정되면 만료 시간이 경과한 후 자동으로 소멸됩니다."""
        now = self._now()
        expire_at = now + ttl if ttl is not None else None
        
        change_entry = {"v": value, "e": expire_at, "del": False}

        if self._tx_stack:
            # 현재 트랜잭션이 열려있으면 해당 프레임에 기록
            self._tx_stack[-1][key] = change_entry
        else:
            # 트랜잭션이 없으면 직접 Base에 기록
            self._store[key] = change_entry
            
        self._set_count += 1

    def get(self, key: str, default=None) -> Any:
        """키의 현재 값을 조회합니다. 키가 없거나 만료된 경우 default를 반환합니다."""
        value, is_live = self._resolve_value(key)
        return value if is_live else default

    def delete(self, key: str) -> bool:
        """키를 삭제합니다. 성공하면 True, 키가 없거나 이미 만료된 경우 False를 반환합니다."""
        _, was_live = self._resolve_value(key)
        if not was_live:
            return False
            
        change_entry = {"v": None, "e": None, "del": True}
        
        if self._tx_stack:
            self._tx_stack[-1][key] = change_entry
        else:
            # Base에서 직접 제거하되, TTL 만료로 인해 논리적으로만 사라진 경우까지 
            # 삭제 카운트에 포함하지 않으려면 _resolve_value의 was_live가 False여야 함.
            self._store.pop(key, None)
            
        self._delete_count += 1
        return True

    def keys(self, prefix: str = "") -> list[str]:
        """현재 유효한 키 중 지정한 접두사(prefix)를 가지는 키들을 사전순으로 반환합니다."""
        now = self._now()
        result = []
        
        # Base 데이터 확인
        for k, v in self._store.items():
            if k.startswith(prefix) and not self._is_expired(v.get("e")):
                result.append(k)
                
        # 트랜잭션 프레임에서 Base를 오버라이드한 키들 확인 (중복 제거 및 우선순위 처리)
        # 하위 TX의 변경이 이미 커밋되어 Base에 반영되었으므로, 현재 활성화된 TX만 스캔하면 충분합니다.
        if self._tx_stack:
            current_frame = self._tx_stack[-1]
            for k, v in current_frame.items():
                if k.startswith(prefix) and not v["del"] and not self._is_expired(v.get("e")):
                    if k not in result: # Base에 없거나 TX에서 갱신된 경우 추가
                        result.append(k)
                        
        return sorted(result)

    def begin(self) -> None:
        """트랜잭션을 시작합니다. 중첩(중복 호출)이 가능합니다."""
        self._tx_stack.append({})

    def commit(self) -> None:
        """가장 안쪽의 트랜잭션을 커밋하여 변경 사항을 하단 레이어(Base 또는 상위 TX)에 반영합니다."""
        if not self._tx_stack:
            raise RuntimeError("커밋할 트랜잭션이 없습니다.")
            
        frame = self._tx_stack.pop()
        
        # 변경사항을 Base로 병합
        for k, change in frame.items():
            if change["del"]:
                self._store.pop(k, None)
            else:
                self._store[k] = {"v": change["v"], "e": change["e"]}
                
        # 하위 중첩 TX 프레임에서 해당 키의 오버라이드를 제거하여 일관성 유지
        for lower_frame in reversed(self._tx_stack[:-1]):
            lower_frame.pop(k, None)

    def rollback(self) -> None:
        """가장 안쪽의 트랜잭션을 롤백합니다. 모든 변경사항이 취소됩니다."""
        if not self._tx_stack:
            raise RuntimeError("롤백할 트랜잭션이 없습니다.")
        self._tx_stack.pop()

    def snapshot(self) -> str:
        """커밋된 상태(Base 데이터)의 유효한 키-값 및 남은 TTL을 JSON 문자열로 반환합니다."""
        now = self._now()
        live_data = []
        
        for k, v in self._store.items():
            if not self._is_expired(v.get("e")):
                remaining_ttl = v["e"] - now if v["e"] is not None else None
                # 값은 JSON 직렬화 가능하다고 가정
                live_data.append({
                    "key": k,
                    "value": v["v"],
                    "ttl_remaining": remaining_ttl
                })
                
        return json.dumps(live_data, ensure_ascii=False)

    @classmethod
    def restore(cls, data: str, clock=None) -> "KVStore":
        """JSON 스냅샷에서 새 KVStore 인스턴스를 복원합니다. TTL은 복원 시점 기준으로 재계산됩니다."""
        store = cls(clock=clock)
        now = store._now()
        
        try:
            items = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError("잘못된 JSON 스냅샷 데이터입니다.") from e
            
        for item in items:
            key = item["key"]
            value = item["value"]
            remaining = item.get("ttl_remaining")
            
            if remaining is not None and remaining > 0:
                new_expire_at = now + remaining
            else:
                new_expire_at = None
                
            store._store[key] = {"v": value, "e": new_expire_at}
        return store

    def stats(self) -> dict[str, int]:
        """저장소의 현재 통계 정보를 반환합니다."""
        now = self._now()
        # Base에 저장된 키 중 실제 살아있는(만료되지 않은) 키 수 세기
        live_base_keys = sum(1 for v in self._store.values() if not self._is_expired(v.get("e")))
        
        return {
            "keys": live_base_keys,
            "sets": self._set_count,
            "deletes": self._delete_count,
            "depth": len(self._tx_stack)
        }
```