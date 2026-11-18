파이썬 클래스 `LRUCache` 를 작성하라.

- `LRUCache(capacity: int)` — capacity 는 0 이상.
- `get(key) -> int` — 있으면 값, 없으면 -1. 조회한 키는 가장 최근 사용으로 갱신한다.
- `put(key, value) -> None` — 값을 넣거나 갱신하고 가장 최근 사용으로 만든다. 용량을 넘으면 가장 오래 사용하지 않은 키를 지운다.
- capacity 가 0 이면 아무것도 저장하지 않는다.
- get/put 은 평균 O(1) 이어야 한다. `functools.lru_cache` 는 쓰지 마라.

설명은 짧게 하고, 최종 코드는 하나의 ```python 코드 블록으로 마지막에 제시하라.
