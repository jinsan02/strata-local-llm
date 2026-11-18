해시 딕셔너리와 가짜 머리(head)/꼬리(tail) 노드를 갖춘 **이중 연결 리스트**를 조합하여 구현합니다. 딕셔너리는 키 조회를 `O(1)`로 처리하고, 연결 리스트의 포인터 조작만으로 요소의 최신 순서 이동과 LRU 제거도 `O(1)`에 수행됩니다. `capacity`가 0인 경우 즉시 저장 작업을 중단하도록 처리했습니다.

```python
class _Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, _Node] = {}
        
        # 더미(head/tail) 노드를 사용하여 경계 조건 처리를 단순화합니다.
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        """연결 리스트에서 노드를 분리합니다."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: _Node) -> None:
        """노드를 헤드 바로 뒤(최신 사용 위치)에 삽입합니다."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # 기존 키: 값 갱신 및 최신 위치로 이동
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
        else:
            # capacity 0 이면 즉시 저장하지 않음
            if self.capacity == 0:
                return
                
            # 용량 초과 시 가장 오래된 노드(tail.prev) 삭제
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
                
            # 새 노드 삽입
            new_node = _Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
```