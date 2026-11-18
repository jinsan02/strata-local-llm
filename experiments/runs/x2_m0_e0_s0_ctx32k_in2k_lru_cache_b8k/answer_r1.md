해시 맵(`dict`)과 이중 연결 리스트(Double Linked List)를 결합한 전형적인 LRU Cache 구조입니다. 해시 맵은 키를 O(1)에 찾도록 저장하고, 연결 리스트는 사용 순서를 유지합니다. 더미(Dummy) 헤드와 테일 노드를 사용해 공백 상태나 양 끝 삽입/삭제 시 예외 처리 없이统一된 로직으로 동작하도록 설계했습니다. `capacity`가 0인 경우 `put`에서 즉시 리턴하며, 조회(`get`)는 해당 노드를 리스트 맨 앞으로 이동시킵니다. 용량 초과 시 꼬리(Tail)의 노드를 제거해 Least Recently Used 항목을 자연스럽게 지웁니다.

```python
class LRUCache:
    class Node:
        __slots__ = 'key', 'value', 'prev', 'next'
        
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.size = 0
        self.head = self.Node()
        self.tail = self.Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self):
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key, value) -> None:
        if self.capacity <= 0:
            return
        
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = self.Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            self.size += 1
            
            if self.size > self.capacity:
                tail_node = self._pop_tail()
                del self.cache[tail_node.key]
                self.size -= 1
```