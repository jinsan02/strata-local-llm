LRU Cache는 `해시맵(dict)`과 `더블리링크드리스트`를 조합하여 구현합니다.
- **해시맵**: 키 → 노드 참조를 저장하여 O(1) 조회/갱신 가능
- **더블리링크드리스트**: 사용 순서를 관리. 머리(`head`)는 최신 사용, 꼬리(`tail`)는 가장 오래된 사용 위치
- `get`/`put` 시 해당 노드를 리스트 머리 바로 뒤로 이동시켜 MRU 갱신, 용량 초과 시 tail 직전(LRU) 노드 제거

```python
class Node:
    __slots__ = 'key', 'value', 'prev', 'next'
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        if capacity <= 0:
            self.cache = {}
            return
            
        self.cache = {}
        self.size = 0
        self.dummy_head = Node()  # Most Recently Used 기준점
        self.dummy_tail = Node()  # Least Recently Used 기준점
        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.prev = self.dummy_head

    def _add_to_front(self, node: Node) -> None:
        """노드를 head 바로 뒤(MRU 위치)에 삽입"""
        node.prev = self.dummy_head
        node.next = self.dummy_head.next
        self.dummy_head.next.prev = node
        self.dummy_head.next = node

    def _remove(self, node: Node) -> None:
        """리스트에서 특정 노드 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _pop_back(self) -> None:
        """tail 직전(LRU) 노드를 제거 및 해시맵에서 삭제"""
        lru_node = self.dummy_tail.prev
        if lru_node and lru_node != self.dummy_head:
            del self.cache[lru_node.key]
            self._remove(lru_node)
            self.size -= 1

    def get