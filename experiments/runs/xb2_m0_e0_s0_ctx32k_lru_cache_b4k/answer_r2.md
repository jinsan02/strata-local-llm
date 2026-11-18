해시맵(`dict`)과 이중 연결리스트를 결합하여 구현합니다.
- **해시맵**: 키로 O(1) 탐색 및 노드 접근
- **이중 연결리스트**: 사용 순서 유지, 헤드(O(1) 삽입/재배치)와 테일(O(1) 삭제)에서 동작
- 더미 헤드/테일 노드를 두어 경계 조건(if-check)을 제거하고 코드 간결성 확보
- `capacity <= 0`이면 즉시 반환하여 저장하지 않도록 처리

```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        # 더미 노드: 가장 최근(head)과 가장 오래된(tail) 위치 고정
        self.head = Node()  # dummy head
        self.tail = Node()  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self):
        node = self.tail.prev
        if node is not self.head:
            self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
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
                tail_node = self._pop_tail()
                del self.cache[tail_node.key]
```