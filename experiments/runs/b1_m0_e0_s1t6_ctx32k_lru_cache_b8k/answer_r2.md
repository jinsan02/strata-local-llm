해시 맵(dict)과 양방향 연결리스트를 결합하여 구현합니다. 
- 해시 맵은 키를 `O(1)`에 탐색하고 해당 노드의 참조를 저장합니다.
- 연결리스트는 사용 순서를 유지하며, 더미(head/tail) 노드를 활용해 경계 조건을 제거했습니다.
- 조회(`get`) 또는 삽입/갱신(`put`) 시 해당 노드를 리스트 맨 뒤(최신 사용)로 이동시키고, 용량 초과 시 맨 앞(LRU) 노드를 삭제합니다.
- `capacity <= 0`인 경우 즉시 반환/종료하도록 분기 처리했습니다.

```python
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        
        # 경계 조건 제거를 위한 더미 노드
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_end(self, node: Node) -> None:
        prev_node = self.tail.prev
        prev_node.next = node
        self.tail.prev = node
        node.prev = prev_node
        node.next = self.tail

    def _remove(self, node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def get(self, key: int) -> int:
        if self.capacity <= 0:
            return -1
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_end(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_end(node)
        else:
            if len(self.cache) == self.capacity:
                lru = self.head.next
                self._remove(lru)
                del self.cache[lru.key]
                
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_end(new_node)
```