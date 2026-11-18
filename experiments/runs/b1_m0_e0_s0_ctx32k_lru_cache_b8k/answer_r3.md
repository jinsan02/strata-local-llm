해시맵(사전)과 더블리 링크드 리스트를 결합하여 구현합니다. 해시맵은 키의 O(1) 탐색을 담당하고, 리스트는 `head`(가장 최근 사용)와 `tail`(가장 오래 사용) 더미 노드로 양 끝에서 삽입/삭제를 모두 O(1)에 처리합니다. `capacity`가 0인 경우 초기화 시 플래그를 설정해 조회/저장 메서드에서 즉시 반환하거나 무시하도록 분기 처리했습니다.

```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            self.capacity = 0
            return
            
        self.capacity = capacity
        self.cache = {}
        self.size = 0
        
        # head: MRU 직후 위치, tail: LRU 직전 위치 (더미 노드)
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: Node):
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node:
        res = self.tail.prev
        self._remove_node(res)
        return res

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
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            self.size += 1
            
            if self.size > self.capacity:
                tail_node = self._pop_tail()
                del self.cache[tail_node.key]
                self.size -= 1
```