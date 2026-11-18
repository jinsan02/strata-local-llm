### 구현 요약
- `collections.OrderedDict`를 내부 저장소로 사용합니다. 딕셔너리는 해싱 기반의 O(1) 평균 접근/삽입 속도를 제공하며, `OrderedDict`는 키가 추가되거나 `move_to_end()`로 이동될 때 삽입 순서를 유지합니다.
- **`get`**: 키가 없으면 `-1`을 반환합니다. 있으면 값을 반환한 후 `move_to_end(key)`로 직전 접근 위치로 이동시켜 "최근 사용"으로 표시합니다.
- **`put`**: `capacity <= 0`이면 즉시 종료하여 저장하지 않습니다. 기존 키라면 순서를 갱신하고 값을 덮씁니다. 새 키면 추가한 뒤, 용량을 초과하면 가장 오래된 항목(`popitem(last=False)`)을 제거합니다.
- 모든 연산이 해시 테이블과 연결 리스트 역할을 수행하는 내부 구조를 통해 평균 O(1) 시간 복잡도를 만족합니다.

### 최종 코드
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        # 접근 시 최신 순서로 이동
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value) -> None:
        # capacity가 0이면 절대 저장하지 않음
        if self.capacity <= 0:
            return
            
        if key in self.cache:
            # 기존 키는 순서만 갱신하고 값 업데이트
            self.cache.move_to_end(key)
        else:
            # 새 키 추가 시 용량 초과 검사 및 LRU eviction
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)  # 가장 오래된 항목 제거
        self.cache[key] = value
```