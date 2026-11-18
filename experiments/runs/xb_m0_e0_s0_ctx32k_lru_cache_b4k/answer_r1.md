### 핵심 아이디어
해시 맵(`dict`)과 이중 연결 리스트(Doubly Linked List)를 조합하여 구현합니다.
- **해시 맵**: O(1) 시간으로 키 존재 여부 확인 및 노드 참조
- **이중 연결 리스트**: 사용 순서(MRU ↔ LRU)를 O(1)로 유지하며, 헤드/테일 더미 노드로 경계 조건을 제거
- `capacity == 0`일 경우 `put`에서 즉시 반환하여 저장 공간을 낭비하지 않음

---

```python
class Node:
    __slots__ = 'key', 'value', 'prev', 'next'
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        
        # 더미 헤드/테일 노드로 공백 및 단일 원소 처리 간소화
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add(self, node: Node) -> None:
        """가장 최근 사용 위치(테일 바로 앞)에 노드 추가"""
        prev_node = self.tail.prev
        next_node = self.tail
        prev_node.next = node
        node.prev = prev_node
        node.next = next_node
        next_node.prev = node

    def _remove(self, node: Node) -> None:
        """연결 리스트에서 노드 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove(node)
        self._add(node)  # 사용했으므로 가장 최근 위치로 이동
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add(node)
        else:
            if len(self.cache) >= self.capacity:
                # 가장 오래 사용하지 않은 키(헤드 바로 뒤) 제거
                lru_node = self.head.next
                self._remove(lru_node)
                del self.cache[lru_node.key]
            
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)
```