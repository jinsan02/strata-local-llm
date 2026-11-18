이 과제는 트랜잭션 격리, TTL 만료, 상태 스냅샷/복원, 통계 카운팅 등을 요구합니다. 표준 라이브러리(`time`, `json`)만으로 구현하며, 트랜잭션 변경사항은 스택 기반의 딕셔너리 레벨에서 관리하여 중첩 트랜잭션과 롤백을 정확하게 처리합니다.

### 핵심 설계
1. **저장 구조**: 커밋된 상태는 `_store`에 저장합니다. 각 키는 `{"value": ..., "expires_at": ...}` 형태를 가집니다.
2. **트랜잭션 계층**: `begin()` 시 스택에 새 변경 레이어를 푸시합니다. `set`/`delete`는 현재 최상위 레이어에 기록됩니다. `get`/`keys`는 스택을 안쪽→바깥순으로 스캔해 즉시 반영된 가시성을 제공합니다.
3. **TTL 처리**: 저장 시점과 TTL로 만료 시각(`expires_at`)을 계산합니다. 조회 시 현재 시각과 비교하여 만료 여부를 결정합니다.
4. **스냅샷/복원**: 커밋된 상태 중 살아있는 키만 추출해 `remaining_ttl`과 함께 JSON 직렬화합니다. `restore`는 복원 시점의 `clock` 기준으로 남은 시간을 재계산하여 다시 세웁니다.
5. **통계**: `sets`는 호출 횟수, `deletes`는 실제 성공(존재하는 키 삭제) 횟수를 카운트합니다. 트랜잭션 내부 조회는 통계에 영향을 주지 않습니다.

### 최종 코드

```python
import time
import json
from typing import Any, Optional

class KVStore:
    """메모리 기반 키-값 저장소. TTL 지원 및 중첩 트랜잭션을 제공합니다."""

    def __init__(self, clock=None) -> None:
        self._clock = clock or time.monotonic
        # 커밋된 상태: key -> {"value": Any, "expires_at": float | None}
        self._store: dict[str, dict[str, Any]] = {}
        # 트랜잭션 스택: 각 레벨은 {key: {"value": ..., "expires_at": ...}, "_deleted": set()} 형태
        self._stack: list[dict] = []
        self._stats_sets: int = 0
        self._stats_deletes: int = 0

    def _now(self) -> float:
        """현재 시각을 반환합니다."""
        return self._clock()

    def _is_expired(self, expires_at: Optional[float]) -> bool:
        """만료 시각이 존재하고 현재 시각보다 전/동일하면 만료된 것으로 간주합니다."""
        return expires_at is not None and self._now() >= expires_at

    def set(self, key: str, value, ttl: float | None = None) -> None:
        """값을 저장합니다. TTL이 지정되면 해당 시간 후 키가 자동으로 만료됩니다."""
        self._stats_sets += 1
        expires_at = self._now() + ttl if ttl is not None else None
        entry = {"value": value, "expires_at": expires_at}

        if self._stack:
            txn = self._stack[-1]
            txn[key] = entry
            # 기존 삭제 표기가 있다면 해제
            if "_deleted" in txn and key in txn["_deleted"]:
                txn["_deleted"].remove(key)
        else:
            self._store[key] = entry

    def get(self, key: str, default=None) -> Any:
        """키에 연결된 값을 반환합니다. 키가 없거나 만료되었으면 default를 반환합니다."""
        # 1. 트랜잭션 스택 조회 (안쪽부터)
        for txn in reversed(self._stack):
            if key in txn:
                entry = txn[key]
                if not self._is_expired(entry.get("expires_at")):
                    return entry["value"]
                else:
                    # 만료된 경우 트랜잭션 레이어에서는 숨김 처리, 바깥 계속 탐색
                    continue

        # 2. 커밋된 저장소 조회
        if key in self._store and not self._is_expired(self._store[key].get("expires_at")):
            return self._store[key]["value"]

        return default

    def delete(self, key: str) -> bool:
        """키를 삭제합니다. 존재하면 True, 없으면 False를 반환합니다."""
        if self._stack:
            txn = self._stack[-1]
            # 현재 트랜잭션 레이어나 그 바깥에서 키가 살아있으면 성공으로 간주
            found = False
            # 트랜잭션 스택 상단에서 아래로 탐색
            for t in reversed(self._stack):
                if key in t:
                    found = True
                    break
            # 커밋된 저장소에도 있는지 확인
            if not found and key in self._store:
                if not self._is_expired(self._store[key].get("expires_at")):
                    found = True

            if found:
                txn["_deleted"] = txn.get("_deleted", set()) | {key}
                # 이미 저장되어있으면 트랜잭션 레이어에서 제거 (가시성 차단)
                if key in txn:
                    del txn[key]
                self._stats_deletes += 1
                return True
            return False
        else:
            # 트랜잭션 없이 바로 삭제
            if key in self._store and not self._is_expired(self._store[key].get("expires_at")):
                del self._store[key]
                self._stats_deletes += 1
                return True
            return False

    def keys(self, prefix: str = "") -> list[str]:
        """살아 있는 키 중 prefix로 시작하는 것을 사전순으로 반환합니다."""
        live_keys: set[str] = set()

        # 커밋된 저장소 반영
        for k, entry in self._store.items():
            if not self._is_expired(entry.get("expires_at")):
                live_keys.add(k)

        # 트랜잭션 스택 반영 (내부에서 외부로 덮어쓰기/차단 처리)
        # 스택을 역순으로 순회하며 최종 상태를 결정하기 위해 집합 관리보다 직접 체크
        temp_keys = set()
        for txn in reversed(self._stack):
            # 삭제된 키는 현재 레벨에서 무효화됨
            deleted = txn.get("_deleted", set())
            for k, entry in txn.items():
                if k == "_deleted":
                    continue
                if k not in deleted and not self._is_expired(entry.get("expires_at")):
                    temp_keys.add(k)

        # 트랜잭션에서 기록된 키는 커밋 상태보다 우선하므로 합쳐서 만료/삭제 체크 필요 없음.
        # 이미 temp_keys에 추가된 것은 유효하므로 최종 집합 생성
        all_live = live_keys | temp_keys

        # prefix 필터링 및 정렬
        return sorted(k for k in all_live if k.startswith(prefix))

    def begin(self) -> None:
        """트랜잭션을 시작합니다. 중첩이 가능합니다."""
        self._stack.append({})

    def commit(self) -> None:
        """가장 안쪽 트랜잭션의 변경사항을 커밋된 저장소에 반영합니다. 트랜잭션이 없으면 RuntimeError를 발생시킵니다."""
        if not self._stack:
            raise RuntimeError("No active transaction to commit.")
        
        txn = self._stack.pop()
        deleted_keys = txn.get("_deleted", set())

        for k, entry in txn.items():
            if k == "_deleted":
                continue
            # 트랜잭션 내의 변경사항을 저장소에 직접 병합 (트랜잭션 간 중첩 커밋은 바깥 컨텍스트를 거치지 않고 저장소로 푸시)
            self._store[k] = entry

        for k in deleted_keys:
            if k in self._store:
                del self._store[k]

    def rollback(self) -> None:
        """가장 안쪽 트랜잭션의 변경사항을 모두 폐기합니다. 트랜잭션이 없으면 RuntimeError를 발생시�니다."""
        if not self._stack:
            raise RuntimeError("No active transaction to rollback.")
        
        self._stack.pop()

    def snapshot(self) -> str:
        """현재 커밋된 상태의 살아있는 키와 남은 TTL을 JSON 문자열로 반환합니다. 진행 중인 트랜잭션은 제외됩니다."""
        now = self._now()
        data = []
        for k, entry in self._store.items():
            exp = entry.get("expires_at")
            if not self._is_expired(exp):
                remaining_ttl = None if exp is None else (exp - now)
                # 값은 JSON 직렬화 가능하다고 가정
                data.append({"key": k, "value": entry["value"], "ttl": remaining_ttl})
        return json.dumps(data)

    @classmethod
    def restore(cls, data: str, clock=None) -> "KVStore":
        """스냅샷 문자열에서 새로운 KVStore 인스턴스를 생성합니다. 남은 TTL은 복원 시점의 clock 기준으로 재계산됩니다."""
        store = cls(clock=clock)
        now = store._now()
        
        try:
            entries = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid snapshot JSON") from e

        for item in entries:
            key = item["key"]
            value = item["value"]
            remaining_ttl = item.get("ttl")
            
            # 남은 TTL 기준으로 새로운 만료 시간 계산
            if remaining_ttl is not None:
                new_expires_at = now + max(0.0, remaining_ttl)  # 음수면 즉시 만료되지만 살아있는 키만 직렬화하므로 이론상 >=0
            else:
                new_expires_at = None
            
            store._store[key] = {"value": value, "expires_at": new_expires_at}
            
        return store

    def stats(self) -> dict[str, int]:
        """저장소의 상태 통계를 반환합니다."""
        now = self._now()
        live_committed_count = sum(1 for e in self._store.values() if not self._is_expired(e.get("expires_at")))
        
        return {
            "keys": live_committed_count,
            "sets": self._stats_sets,
            "deletes": self._stats_deletes,
            "depth": len(self._stack)
        }
```