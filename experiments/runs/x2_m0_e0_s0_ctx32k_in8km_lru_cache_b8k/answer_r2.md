해시 테이블(`dict`)과 양방향 연결 리스트를 조합한 표준 구현입니다. 사전은 키 탐색을 O(1)로, 연결 리스트는 가장 최근/오래된 노드의 삽입·삭제를 O(1)로 처리하여 평균 시간복잡도를 보장합니다. `capacity`가 0인 경우 연산 내내 즉시 반환되도록 하여 불필요한 저장 및 링크 조정을 방지합니다.

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
        self._capacity = max(0, capacity)
        self._cache: dict = {}
        
        # 더미 헤드(가장 최근 사용 쪽)와 더미 테일(가장 오래된 사용 쪽) 연결 리스트 초기화
        self._dummy_head = _Node()
        self._dummy_tail = _Node()
        self._dummy_head.next = self._dummy_tail
        self._dummy_tail.prev = self._dummy_head

    def _remove_node(self, node: _Node) -> None:
        """연결 리스트에서 노드를 제거합니다."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: _Node) -> None:
        """더미 헤드 뒤에 노드를 삽입(가장 최근 사용 위치)합니다."""
        node.prev = self._dummy_head
        node.next = self._dummy_head.next
        self._dummy_head.next.prev = node
        self._dummy_head.next = node

    def get(self, key) -> int:
        if self._capacity == 0 or key not in self._cache:
            return -1
        
        node = self._cache[key]
        self._remove_node(node)
        self._add_to_front(node)
        return node.value

    def put(self, key, value) -> None:
        if self._capacity == 0:
            return

        if key in self._cache:
            node = self._cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_front(node)
        else:
            new_node = _Node(key, value)
            self._cache[key] = new_node
            self._add_to_front(new_node)

            if len(self._cache) > self._capacity:
                # 가장 오래된 노드(테일 바로 앞) 제거
                evict_node = self._dummy_tail.prev
                self._remove_node(evict_node)
                del self._cache[evict_node.key]
```