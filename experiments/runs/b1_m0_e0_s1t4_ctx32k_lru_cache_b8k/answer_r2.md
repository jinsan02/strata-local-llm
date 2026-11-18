해시맵(`self.cache`)과 양방향 연결리스트를 조합하여 구현합니다. 해시맵은 O(1) 시간으로 키-노드를 찾도록 하고, 연결리스트는 사용 순서를 유지합니다. 더미 `head`(최신 사용 측)와 `tail`(가장 오래된 사용 측) 노드를 두어 삽입/삭제 로직을 경계 조건 없이 깔끔하게 처리합니다.

- `get`: 키 존재 시 해당 노드를 `head` 바로 뒤로 이동(MRU 갱신) 후 값 반환
- `put`: 기존 키면 값 변경 후 MRU 이동, 신규 키면 리스트에 추가 후 용량 초과 시 `tail` 직전(LRU) 노드 삭제
- `capacity == 0`인 경우 즉시 `-1` 반환 또는 저장 생략 처리하여 제약 조건 충족
- 모든 연산은 해시 조회 + 포인터 재할당만으로 구성되므로 평균 O(1) 보장

```python
class _Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key: int = -1, val: int = -1):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        self.head = _Node()  # MRU 더미
        self.tail = _Node()  # LRU 더미
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add(self, node: _Node) -> None:
        # head 바로 뒤 (가장 최근 사용 위치) 삽입
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: _Node) -> None:
        self._remove(node)
        self._add(node)

    def _pop_tail(self) -> _Node:
        # LRU 노드 (tail 직전) 제거 및 반환
        res = self.tail.prev
        self._remove(res)
        return res

    def get(self, key: int) -> int:
        if self.capacity == 0 or key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._move_to_head(node)
        else:
            new_node = _Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]
```