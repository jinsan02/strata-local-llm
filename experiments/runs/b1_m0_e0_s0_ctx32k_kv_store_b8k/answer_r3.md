```python
import copy
import json
import time
from typing import Any, Callable


class KVStore:
    """TTL 지원 및 중첩 트랜잭션이 가능한 인메모리 키-값 저장소."""

    def __init__(self, clock: Callable[[], float] | None = None) -> None:
        self._clock = clock or time.monotonic
        # 현재 전체 상태 (커밋된 상태 + 활성 트랜잭션 변경사항 포함)
        self._state: dict[str, dict] = {}
        # 커밋된 영구 상태 (snapshot/restore 용도)
        self._committed: dict[str, dict] = {}
        # 트랜잭션 레벨별 변경 로그 스택. 각 요소는 [(key, original_info), ...] 형태
        self._tx_stack: list[list[tuple[str, dict | None]]] = []

        # 통계 카운터
        self._sets_count: int = 0
        self._deletes_count: int: int = 0

    def _now(self) -> float:
        return self._clock()

    def _is_expired(self, expire_at: float | None) -> bool:
        if expire_at is None:
            return False
        return self._now() >= expire_at

    def _purge_if_expired(self, key: str) -> dict | None:
        """키가 만료되었으면 저장소에서 제거하고 None을 반환. 아니면 값/만료정보를 반환."""
        info = self._state.get(key)
        if info is None or self._is_expired(info["e"]):
            self._state.pop(key, None)
            return None
        return info

    # ------------------------------------------------------------------ #
    #                        공개 메서드                                   #
    # ------------------------------------------------------------------ #
    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """값을 저장한다. ttl이 제공되면 지정 시간 후 자동 만료된다."""
        expire_at = self._now() + ttl if ttl is not None else None
        old_info = self._purge_if_expired(key)

        self._state[key] = {"v": value, "e": expire_at}
        if self._tx_stack:
            self._tx_stack[-1].append((key, old_info))
        self._sets_count += 1

    def get(self, key: str, default: Any = None) -> Any | None:
        """키에 대한 값을 반환한다. 없거나 만료되었으면 default를 반환."""
        info = self._purge_if_expired(key)
        return info["v"] if info else default

    def delete(self, key: str) -> bool:
        """키를 삭제한다. 성공 시 True, 키가 없거나 이미 만료되었으면 False."""
        old_info = self._state.get(key)
        if old_info is None or self._is_expired(old_info["e"]):
            self._state.pop(key, None)
            return False

        del self._state[key]
        self._deletes_count += 1
        if self._tx_stack:
            self._tx_stack[-1].append((key, old_info))
        return True

    def keys(self, prefix: str = "") -> list[str]:
        """현재 유효한(key이 만료되지 않은) 키 중 prefix로 시작하는 것들을 사전순으로 반환."""
        now = self._now()
        valid_keys = [
            k for k, info in self._state.items()
            if k.startswith(prefix) and not self._is_expired(info["e"])
        ]
        return sorted(valid_keys)

    def begin(self) -> None:
        """새로운 트랜잭션을 시작한다. 중첩 호출이 가능하다."""
        self._tx_stack.append([])

    def commit(self) -> None:
        """가장 안쪽 트랜잭션의 변경사항을 커밋된 상태로 반영한다."""
        if not self._tx_stack:
            raise RuntimeError("트랜잭션이 활성화되어 있지 않습니다.")

        changes = self._tx_stack.pop()
        for key, old_info in changes:
            cur = self._state.get(key)
            if old_info is None and cur is not None:
                # 새로 추가된 키
                self._committed[key] = copy.deepcopy(cur)
            elif old_info is not None:
                if cur is None:
                    # 삭제됨
                    self._committed.pop(key, None)
                else:
                    # 수정됨
                    self._committed[key] = copy.deepcopy(cur)

    def rollback(self) -> None:
        """가장 안쪽 트랜잭션의 변경사항을 모두 취소한다."""
        if not self._tx_stack:
            raise RuntimeError("트랜잭션이 활성화되어 있지 않습니다.")

        changes = self._tx_stack.pop()
        for key, old_info in changes:
            if old_info is None:
                # 트랜잭션 중 새로 추가된 키는 제거
                self._state.pop(key, None)
            else:
                # 기존 상태로 복원
                self._state[key] = copy.deepcopy(old_info)

    def snapshot(self) -> str:
        """현재 커밋된 상태의 살아있는 키와 남은 TTL을 JSON 문자열로 반환한다."""
        now = self._now()
        payload: dict[str, dict] = {}
        for key, info in self._committed.items():
            expire_at = info["e"]
            if expire_at is None or now < expire_at:
                remaining_ttl = (expire_at - now) if expire_at else None
                payload[key] = {
                    "value": info["v"],
                    "remaining_ttl": round(remaining_ttl, 3) if remaining_ttl is not None else None
                }
        return json.dumps(payload, ensure_ascii=False)

    @classmethod
    def restore(cls, data: str, clock: Callable[[], float] | None = None) -> "KVStore":
        """snapshot 문자열을 역직렬화하여 새 KVStore 인스턴스를 생성한다."""
        store = cls(clock=clock)
        payload = json.loads(data)
        now = store._now()
        for key, node in payload.items():
            value = node["value"]
            rem_ttl = node.get("remaining_ttl")
            if rem_ttl is None:
                expire_at = None
            else:
                # 복원 시점에서부터 남은 시간만큼 TTL을 재설정
                expire_at = now + rem_ttl
            store._committed[key] = {"v": value, "e": expire_at}
            store._state[key] = {"v": value, "e": expire_at}
        return store

    def stats(self) -> dict[str, int]:
        """저장소의 상태 통계를 반환한다."""
        # 살아있는 커밋된 키 수 계산 (만료 제외)
        now = self._now()
        live_committed_keys = sum(
            1 for info in self._committed.values()
            if info["e"] is None or now < info["e"]
        )
        return {
            "keys": live_committed_keys,
            "sets": self._sets_count,
            "deletes": self._deletes_count,
            "depth": len(self._tx_stack)
        }
```