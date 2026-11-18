해당 과제는 대표적인 알고리즘 문제인 **LRU(Cache Replacement Policy)** 구현입니다. 평균 O(1) 시간 복잡도를 보장하려면 **해시맵(Dict)**으로 키 조회를 빠르게 처리하고, **양방향 연결리스트(Double Linked List)**로 사용 순서(접근 위치 이동/최신 데이터 교체/가장 오래된 데이터 삭제)를 O(1)에 관리해야 합니다.

- `capacity == 0`일 경우 저장 공간을 아예 할당하지 않고 `put`은 즉시 반환, `get`은 항상 `-1`을 리턴하도록 처리합니다.
- 더미(head/tail) 노드를 사용해 경계 조건(`empty`, `full`)에서의 분기 로직을 제거하여 코드를 간결하게 유지했습니다.

```python
class _Node:
    __slots__ = 'key', 'value', 'prev', 'next'
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = max(0, capacity)  # 음수 방지 및 0 지원
        self.cache = {}                   # key -> _Node 매핑 (O(1) 조회)
        self.size = 0

        # 양방향 연결리스트 더미 헤드/테일
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_front(node)
        return node.value

    def put(self, key, value) -> None:
        if self.capacity == 0:
            return

        if key in self.cache:
            # 기존 키: 값 갱신 후 최전방(가장 최근)으로 이동
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
        else:
            # 새 키: 생성 후 최전방에 삽입
            new_node = _Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
            self.size += 1

            # 용량 초과 시 가장 오래된 데이터(테일 바로 앞 노드) 제거
            if self.size > self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
                self.size -= 1

    def _add_to_front(self, node: _Node) -> None:
        """노드를 헤드 바로 뒤에 삽입 (가장 최근 사용 위치)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _remove(self, node: _Node) -> None:
        """연결리스트에서 노드를 제거"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_front(self, node: _Node) -> None:
        """노드를 현재 위치에서 제거 후 최전방으로 재삽입"""
        self._remove(node)
        self._add_to_front(node)
```