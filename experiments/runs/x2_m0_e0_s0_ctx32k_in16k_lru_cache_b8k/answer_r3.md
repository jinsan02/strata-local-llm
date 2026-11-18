### 구현 방식 설명
- **해시맵 + 양방향 연결리스트** 조합으로 평균 O(1) 복잡도를 보장합니다. 해시맵(`dict`)은 키의 상수 시간 탐색을 담당하고, 연결리스트는 접근 순서를 유지하며 노드 삽입/삭제를 상수 시간에 수행합니다.
- **더미 헤드/테일 노드**를 양끝에 배치하여 경계 조건(빈 리스트, 첫/마지막 요소 처리)을 분기 없이統一 처리합니다.
- `capacity == 0`인 경우 즉시 반환하도록 별도 분기를 두어 메모리를 낭비하지 않습니다.
- `functools.lru_cache`를 사용하지 않고 직접 노드 구조체를 구현하였습니다.

```python
class _Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            self.capacity = 0
        else:
            self.capacity = capacity

        self.cache: dict[int, _Node] = {}
        
        # 더미 헤드/테일 노드로 경계 조건 처리 단순화
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: _Node) -> None:
        """맨 앞(가장 최근 사용)에 노드 추가"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove(self, node: _Node) -> None:
        """연결리스트에서 특정 노드 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: _Node) -> None:
        """노드를 맨 앞으로 이동"""
        self._remove(node)
        self._add_to_head(node)

    def _pop_tail(self) -> _Node:
        """맨 뒤(LRU)의 노드 제거 및 반환"""
        res = self.tail.prev
        self._remove(res)
        return res

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

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
                lru = self._pop_tail()
                del self.cache[lru.key]
```