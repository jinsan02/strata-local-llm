해당 구현은 **해시맵(Dict)**과 **양방향 연결 리스트(Double Linked List)**를 결합한 표준 LRU 방식입니다. 해시맵은 키 검색을 `O(1)`에 처리하고, 연결 리스트는 노드의 추가/삭제를 `O(1)`에 수행하며 최근 사용 순서를 유지합니다. `capacity`가 0이면 `put`에서 즉시 반환하여 데이터를 저장하지 않도록 처리합니다.

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
        
        # 더미 노드: head(가장 최근 사용), tail(가장 오래된 사용)
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node) -> None:
        """head 바로 다음에 노드를 추가 (최신 사용으로 표시)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """연결 리스트에서 특정 노드를 분리"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove_node(node)
        self._add_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
        else:
            if len(self.cache) >= self.capacity:
                # LRU 항목( tail 바로 앞) 제거
                lru = self.tail.prev
                self._remove_node(lru)
                del self.cache[lru.key]
                
            node = Node(key, value)
            self.cache[key] = node
            
        self._add_to_head(node)
```