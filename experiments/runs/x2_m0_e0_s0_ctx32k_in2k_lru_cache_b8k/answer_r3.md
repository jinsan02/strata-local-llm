### 구현 설명
- **해시맵 + 이중 연결리스트** 조합으로 구현합니다. 해시맵(`dict`)은 `key → Node` 매핑을 O(1) 만에 처리하고, 연결리스트는 사용 순서(가장 최근 ↔ 가장 오래됨)를 포인터 조작만으로 O(1) 에 관리합니다.
- **더미(Dummy) 헤드/테일 노드**를 배치해 경계 조건(빈 리스트 삽입/제거 등)을统一되게 처리합니다. `get` 호출 시 해당 노드를 항상 헤드 바로 뒤로 이동시켜 '가장 최근 사용'으로 표시하고, `put` 중 용량 초과 시 테일 직전 노드를 제거해 LRU를 배출합니다.
- `capacity <= 0`인 경우 초기화 시 `max(0, capacity)`로 보장하고, 각 메서드 진입 시 즉시 반환하도록 처리해 메모리 할당과 연산을 완전히 차단합니다.
- 모든 탐색, 이동, 삽입/제거가 고정된 포인터 조작 또는 해시 조회이므로 평균 시간 복잡도는 **O(1)**입니다.

```python
class _Node:
    __slots__ = 'key', 'value', 'prev', 'next'
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value


class LRUCache:
    def __init__(self, capacity: int):
        self._capacity = max(0, capacity)
        self._cache = {}  # key -> _Node
        self._head = _Node()  # 더미 헤드
        self._tail = _Node()  # 더미 테일
        self._head.next = self._tail
        self._tail.prev = self._head

    def _add_to_head(self, node):
        """노드를 헤드 바로 뒤에 삽입 (가장 최근 위치)"""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _remove_node(self, node):
        """연결리스트에서 특정 노드를 끊어냅니다."""
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _move_to_head(self, node):
        """노드를 헤드 바로 앞으로 이동합니다."""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self):
        """테일 직전(가장 오래된) 노드를 제거하고 반환합니다."""
        res = self._tail.prev
        self._remove_node(res)
        return res

    def get(self, key: int) -> int:
        if self._capacity <= 0 or key not in self._cache:
            return -1
        node = self._cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self._capacity <= 0:
            return
        if key in self._cache:
            node = self._cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = _Node(key, value)
            self._cache[key] = new_node
            self._add_to_head(new_node)
            if len(self._cache) > self._capacity:
                tail_node = self._pop_tail()
                del self._cache[tail_node.key]
```