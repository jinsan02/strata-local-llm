이 과제는 트랜잭션 지원, TTL 만료, 스냅샷/복원 기능을 갖춘 인메모리 키-값 저장소를 구현하는 것입니다. 표준 라이브러리(`time`, `json`)만 사용하여 단일 클래스로 작성합니다.

### 핵심 설계 사항
1. **TTL 관리**: 내부적으로 절대 만료 시각(`expires_at = 현재시간 + ttl`)으로 저장하고, 접근 시 현재 시각과 비교하여 만료된 키를 자동으로 가립니다. `ttl=None`은 무한정 생존(`float('inf')`)을 의미합니다.
2. **트랜잭션 계층**: `_txn_stack`에 변경 내역을 쌓습니다. `get`/`keys`는 가장 안쪽 트랜잭션부터 탐색하여 최신 상태를 반영하고, 없으면 커밋된 저장소(`_store`)를 조회합니다. `commit()` 시 변경사항을 원본에 병합(apply)하고, `rollback()` 시 스택을 제거합니다.
3. **`None` 값 처리**: 키 존재 여부와 실제 값이 `None`인 경우를 구분하기 위해 `_MISSING`, `_DELETED` 같은 sentinel 객체를 사용합니다.
4. **스냅샷/복원**: 커밋된 상태만 JSON으로 직렬화합니다. `restore` 시 저장된 남은 TTL(duration)을 가져와 복원 직후 시각에 더해 새로운 절대 만료 시각으로 설정합니다.

### 구현 코드

```python
import time
import json
from typing import Any, Optional


class KVStore:
    """트랜잭션 지원 TTL 키-값 저장소 클래스입니다."""

    _MISSING = object()
    _DELETED = object()

    def __init__(self, clock: Optional[callable] = None):
        """
        저장소를 초기화합니다.

        Args:
            clock: 인자 없이 현재 시각(초, float)을 반환하는 callable. 미제공 시 time.monotonic 사용.
        """
        self._clock = clock if clock is not None else time.monotonic
        self._store: dict[str, tuple[Any, float]] = {}  # key -> (value, expires_at)
        self._txn_stack: list[dict[str, Any]] = []      # 트랜잭션별 변경 로그 스택
        self._set_count: int = 0
        self._del_count: int = 0

    def _now(self) -> float:
        """클록에서 현재 시각을 가져옵니다."""
        return self._clock()

    def _is_expired(self, expires_at: float) -> bool:
        """만료 시각이 현재 시각을 지났는지 확인합니다."""
        if expires_at == float('inf'):
            return False
        return expires_at <= self._now()

    def _lookup(self, key: str) -> Any:
        """키를 트랜잭션 계층 및 저장소에서 조회합니다. 없으면 _MISSING 반환."""
        # 안쪽 트랜잭션부터 탐색
        for changes in reversed(self._txn_stack):
            if key in changes:
                val = changes[key]
                if val is self._DELETED:
                    return self._MISSING
                return val

        # 저장소 fallback
        if key in self._store:
            value, exp = self._store[key]
            if not self._is_expired(exp):
                return value

        return self._MISSING

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """
        값을 저장합니다. TTL이 초과되면 키는 유효하지 않게 됩니다.

        Args:
            key:   저장할 키
            value: 저장할 값
            ttl:   초 단위 만료 시간 (None 이면 무제한)
        """
        self._set_count += 1
        now = self._now()
        expires_at = now + ttl if ttl is not None else float('inf')

        if self._txn_stack:
            # 트랜잭션 중이라면 로컬 변경내역에 기록
            self._txn_stack[-1][key] = (value, expires_at)
        else:
            # 직접 저장소에 반영
            self._store[key] = (value, expires_at)

    def get(self, key: str, default: Any = None) -> Any:
        """
        값을 조회합니다. 키가 없거나 만료되었으면 default 를 반환합니다.

        Args:
            key:     조회할 키
            default: 키가 없을 때 반환할 기본값

        Returns:
            저장된 값 또는 default
        """
        res = self._lookup(key)
        return default if res is self._MISSING else res

    def delete(self, key: str) -> bool:
        """
        키를 삭제합니다. 키가 존재하면 True, 없으면 False 를 반환합니다.

        Args:
            key: 삭제할 키

        Returns:
            성공 여부 (bool)
        """
        if self._lookup(key) is not self._MISSING:
            self._del_count += 1
            if self._txn_stack:
                # 트랜잭션 중이면 삭제 마커 기록
                self._txn_stack[-1][key] = self._DELETED
                return True
            else:
                del self._store[key]
                return True
        return False

    def keys(self, prefix: str = "") -> list[str]:
        """
        살아있는 키 중 prefix 로 시작하는 키를 사전순으로 반환합니다.
        트랜잭션 내부의 변경사항도 반영됩니다.

        Args:
            prefix: 필터링 접두사

        Returns:
            정렬된 키 목록
        """
        now = self._now()
        result_keys = set()

        # 1. 커밋된 저장소에서 조건에 맞는 살아있는 키 수집
        for k, (_, exp) in self._store.items():
            if not self._is_expired(exp) and k.startswith(prefix):
                result_keys.add(k)

        # 2. 트랜잭션 변경내역 적용 (안쪽이 최우선)
        for changes in reversed(self._txn_stack):
            for k, v in changes.items():
                if k.startswith(prefix):
                    if v is self._DELETED:
                        result_keys.discard(k)
                    else:
                        result_keys.add(k)

        return sorted(result_keys)

    def begin(self) -> None:
        """트랜잭션을 시작합니다. 중첩 호출 가능합니다."""
        self._txn_stack.append({})

    def commit(self) -> None:
        """가장 안쪽 트랜잭션의 변경사항을 커밋합니다."""
        if not self._txn_stack:
            raise RuntimeError("commit() 은 begin() 이후에만 호출할 수 있습니다.")

        changes = self._txn_stack.pop()
        now = self._now()
        for k, val in changes.items():
            if val is self._DELETED:
                self._store.pop(k, None)
            else:
                self._store[k] = val

    def rollback(self) -> None:
        """가장 안쪽 트랜잭션의 변경사항을 모두 취소합니다."""
        if not self._txn_stack:
            raise RuntimeError("rollback() 은 begin() 이후에만 호출할 수 있습니다.")
        
        self._txn_stack.pop()

    def snapshot(self) -> str:
        """
        현재 커밋된 상태의 살아있는 키와 남은 TTL 을 JSON 문자열로 반환합니다.
        진행 중인 트랜잭션은 포함되지 않습니다.
        """
        now = self._now()
        data = {}
        for k, (v, exp) in self._store.items():
            if not self._is_expired(exp):
                remaining = (exp - now) if exp != float('inf') else None
                data[k] = {"v": v, "t": remaining}

        return json.dumps(data)

    @classmethod
    def restore(cls, data: str, clock: Optional[callable] = None) -> "KVStore":
        """
        snapshot() 으로 직렬화된 문자열에서 새 저장소를 복원합니다.
        남은 TTL 은 복원 시점의 clock 기준으로 다시 계산됩니다.
        """
        inst = cls(clock=clock)
        parsed = json.loads(data)
        
        # 클록이 없으면 default 사용, 있다면 그 현재 시각 기준 
        curr_time = inst._now()
        
        for k, info in parsed.items():
            ttl_duration = info["t"]  # 복원 시점 기준으로 남은 시간 (초)
            # TTL 이 None 이면 무제한, 그렇지 않으면 남은만큼 다시 설정
            inst.set(k, info["v"], ttl_duration)

        return inst

    def stats(self) -> dict:
        """
        저장소 및 트랜잭션 상태를 요약한 딕셔너리를 반환합니다.

        Returns:
            {
                "keys": 살아있는 커밋된 키 수 (int),
                "sets": set() 호출 누적 횟수 (int),
                "deletes": 실제로 삭제에 성공한 delete() 횟수 (int),
                "depth": 현재 열려있는 트랜