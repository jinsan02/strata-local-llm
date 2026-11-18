해시맵과 이중 연결리스트를 결합하여 구현합니다.
- **해시맵**: 키의 O(1) 탐색 및 노드 객체 참조 저장
- **이중 연결리스트**: 더미 head/tail 노드를 활용해 사용 순서(LRU → MRU)를 상수 시간에 이동·삭제
- `capacity <= 0`이면 즉시 리턴하여 저장하지 않도록 처리

```python
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(capacity, 0)
        self.cache = {}  # key -> Node
        
        # 더미 헤드/테일 노드로 경계 조건 제거
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _add_to_head(self, node: Node) -> None:
        """노드를 head 바로 뒤에 삽입 (가장 최근 사용 위치)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """연결리스트에서 특정 노드 제거"""
        prev_n, next_n = node.prev, node.next
        prev_n.next = next_n
        next_n.prev = prev_n

    def _move_to_head(self, node: Node) -> None:
        """노드를 head 바로 앞으로 이동 (최근 사용으로 갱신)"""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node:
        """테일 바로 앞 노드(LRU) 제거 후 반환"""
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key, value) -> None:
        if self.capacity <= 0:
            return  # 저장 불가

        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            self.size += 1

        if self.size > self.capacity:
            lru_node = self._pop_tail()
            del self.cache[lru_node.key]
            self.size -= 1


class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
```