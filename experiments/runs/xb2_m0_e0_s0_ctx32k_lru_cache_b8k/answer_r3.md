해시맵(딕셔너리)과 이중 연결리스트를 결합한 표준 구현입니다.
- **해시맵**: 키 → 노드의 매핑으로 `O(1)` 조회 및 삭제 지원
- **이중 연결리스트**: 사용 순서 유지. 더미 `head`(가장 최근), `tail`(가장 오래됨) 노드를 양끝에 둬서 경계 조건을 제거하고 삽입/삭제를 `O(1)`로 처리
- **capacity 0**: 즉시 `-1` 반환 또는 무시하도록 분리 처리

```python
class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node()  # 더미 헤드 (가장 최근 사용)
        self.tail = Node()  # 더미 테일 (가장 오래되지 않은 사용)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: Node) -> None:
        self._remove(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node:
        node = self.tail.prev
        self._remove(node)
        return node

    def get(self, key: int) -> int:
        if self.capacity == 0:
            return -1
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            if len(self.cache) > self.capacity:
                lru_node = self._pop_tail()
                del self.cache[lru_node.key]
```