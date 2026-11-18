### 구현 설명
해시 맵(`dict`)과 더미 헤드/테일을 가진 양방향 연결리스트를 결합하여 구현합니다. 해시 맵은 키로 노드를 `O(1)`에 찾고, 연결리스트는 삽입/삭제 시 포인터만 재할당하면 되므로 모든 연산이 상수 시간에 동작합니다. 조회(`get`) 또는 삽입(`put`) 시 해당 노드를 리스트의 헤드 바로 뒤로 이동시켜 '가장 최근 사용' 상태를 기록하고, 저장 용량을 초과하면 리스트의 테일 바로 앞 노드(가장 오래 사용하지 않은 키)를 즉시 제거합니다. `capacity <= 0`인 경우 `put`은 무조건 반환하고 `get`은 `-1`을 리턴하여 아무것도 저장하지 않도록 처리합니다.

### 최종 코드
```python
class _Node:
    """양방향 연결리스트의 노드."""
    __slots__ = ('key', 'value', 'prev', 'next')
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = max(capacity, 0)
        self.cache = {}
        
        # 양방향 연결리스트의 고정 기준점 (더미 헤드/테일)
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key) -> int:
        if key in self.cache:
            node = self.cache[key]
            # 조회한 키를 가장 최근 사용 위치로 이동
            self._move_to_head(node)
            return node.value
        return -1

    def put(self, key, value) -> None:
        # 용량이 0이면 저장하지 않음
        if self.capacity <= 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            node = _Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            
            # 용량 초과 시 가장 오래 사용하지 않은 노드(테일 전 노드) 제거
            if len(self.cache) > self.capacity:
                lru = self.tail.prev
                del self.cache[lru.key]
                lru.prev.next = lru.next
                lru.next.prev = lru.prev

    def _add_to_head(self, node: _Node) -> None:
        """헤드 바로 뒤에 노드를 삽입."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: _Node) -> None:
        """리스트에서 노드를 분해."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: _Node) -> None:
        """노드를 리스트 최전방(헤드 바로 뒤)으로 이동."""
        self._remove_node(node)
        self._add_to_head(node)
```