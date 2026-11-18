해시 테이블(`dict`)과 양방향 연결 리스트를 결합한 구조를 사용합니다. `dict`는 키의 O(1) 조회/삽입을 담당하고, 연결 리스트는 사용 순서(최근 ↔ 오래된)를 O(1)로 관리합니다. 더미(dummy) 헤드와 테일을 배치해 경계 조건 처리를 간결하게 하며, `capacity == 0`일 경우 즉시 리턴하도록 초기화 및 메소드 입구에서 분기합니다.

```python
class _Node:
    __slots__ = ('key', 'value', 'prev', 'next')
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("capacity must be >= 0")
        self.capacity = capacity
        self.cache = {}
        self.head = _Node()  # 더미 헤드 (가장 최근 사용 노드 바로 앞)
        self.tail = _Node()  # 더미 테일 (가장 오래된 사용 노드 바로 뒤)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: _Node) -> None:
        """더미 헤드 뒤에 newNode를 삽입 (최신 위치)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: _Node) -> None:
        """연결 리스트에서 node를 완전히 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: _Node) -> None:
        """기존 노드를 헤드 바로 뒤로 이동 (최근 사용으로 갱신)"""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> _Node:
        """테일 바로 앞의 노드(가장 오래된 사용)를 제거하고 반환"""
        target = self.tail.prev
        if target is not self.head:
            self._remove_node(target)
        return target

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
            new_node = _Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            if len(self.cache) > self.capacity:
                evicted = self._pop_tail()
                del self.cache[evicted.key]
```