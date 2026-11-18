### 설명
`dict` 해시 맵으로 키-노드 매핑을 `O(1)`에 조회하고, 이중 연결 리스트로 사용 순서를 유지합니다. 더미(`head`, `tail`) 노드를 배치해 빈 상태나 경계 조건 처리를 간소화했습니다. `get`은 키가 있으면 해당 노드를 머리쪽으로 이동 후 값을 반환하고, 없으면 `-1`을 반환합니다. `put`은 기존 키면 값을 갱신해 머리쪽으로 이동하고, 새 키면 용량 초과 시 꼬리(LRU) 노드를 제거한 뒤 새로 추가합니다. `capacity <= 0`인 경우 즉시 동작을 중단하여 저장하지 않습니다.

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
        
        # 더미 head/tail 노드 배치 (경계 조건 처리 간소화)
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _add_to_head(self, node: Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node) -> None:
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node:
        # tail 직전 노드가 Least Recently Used
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        if self.capacity <= 0 or key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            if self.size >= self.capacity:
                removed = self._pop_tail()
                del self.cache[removed.key]
                self.size -= 1
                
            new_node = Node(key, value)
            self._add_to_head(new_node)
            self.cache[key] = new_node
            self.size += 1
```