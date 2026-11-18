파이썬 모듈 하나로 메모리 키-값 저장소 클래스 `KVStore` 를 작성하라. 이 과제는 **완성된 모듈 전체**를 요구한다.

생성자: `KVStore(clock=None)` — `clock` 은 인자 없이 현재 시각(초, float)을 돌려주는 함수이며, 없으면 `time.monotonic` 을 쓴다.

메서드:
- `set(key: str, value, ttl: float | None = None) -> None` — 값을 저장한다. `ttl` 초가 지나면(현재 시각 >= 저장 시각 + ttl) 없는 키로 취급한다. 다시 `set` 하면 이전 TTL 은 사라진다.
- `get(key: str, default=None)` — 값 또는 `default`.
- `delete(key: str) -> bool` — 지웠으면 True, 없던 키면 False.
- `keys(prefix: str = "") -> list[str]` — 살아 있는 키 중 prefix 로 시작하는 것을 사전순으로.
- `begin() -> None` — 트랜잭션 시작. **중첩**할 수 있다.
- `commit() -> None` — 가장 안쪽 트랜잭션의 변경을 바깥(또는 저장소)에 반영. 트랜잭션이 없으면 `RuntimeError`.
- `rollback() -> None` — 가장 안쪽 트랜잭션의 변경을 버린다. 트랜잭션이 없으면 `RuntimeError`.
- 트랜잭션 안에서의 `get` · `keys` 는 그 트랜잭션까지의 변경(set · delete)을 반영한 상태를 보여야 한다.
- `snapshot() -> str` — 커밋된 상태(진행 중인 트랜잭션 변경 제외)의 살아 있는 키를 JSON 문자열로. 남은 TTL 도 담는다. 값은 JSON 으로 표현 가능한 것만 온다고 가정한다.
- `KVStore.restore(data: str, clock=None) -> KVStore` (classmethod) — `snapshot` 결과에서 새 저장소를 만든다. 남은 TTL 은 복원 시점의 clock 기준으로 다시 센다.
- `stats() -> dict` — `{"keys": 살아 있는 커밋된 키 수, "sets": set 호출 수, "deletes": 실제로 지운 delete 수, "depth": 현재 트랜잭션 깊이}`.

요구:
- 모든 공개 메서드에 타입 힌트와 docstring 을 단다.
- 외부 라이브러리는 쓰지 않는다 (표준 라이브러리만).

설명은 짧게 하고, 최종 코드는 하나의 ```python 코드 블록으로 마지막에 제시하라.
