### 구현 방식 설명
해시 맵(`dict`)과 **더블 리스 링크드 리스트(Double Linked List)**를 조합하여 `O(1)` 평균 시간복잡도를 달성합니다.
- **해시 맵**: 키 → 노드의 매핑을 빠르게 조회/제거하기 위해 사용 (`O(1)`)
- **더블 리스 리스트**: 사용 순서를 유지. 더미 헤드(가장 오래된 항목 근처)와 더미 테일(가장 최근 항목 위치) 사이에 실제 데이터를 관리하여 선두 삽입/끝 제거를 `O(1)`로 처리
- `capacity == 0`인 경우 저장 공간을 할당하지 않고 즉시 동작을 종료하도록 처리

### 코드
```python
class Node:
    __slots__ = ('key', 'value', 'prev', 'next')
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(capacity, 0)
        self.cache = {}
        
        # 더미 헤드(가장 오래된 쪽)와 더미 테일(가장 최근 쪽)
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_end(self, node: Node) -> None:
        """테일 바로 앞에 노드를 삽입 (가장 최근 사용 위치)"""
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def _remove_node(self, node: Node) -> None:
        """리스트에서 노드를 단절"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove_node(node)
        self._add_to_end(node)  # 최근 사용으로 갱신
        return node.value

    def put(self, key, value) -> None:
        if self.capacity <= 0:
            return

        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_end(node)
        else:
            # 용량 초과 시 가장 오래된 항목(head.next) 제거
            if len(self.cache) >= self.capacity:
                lru = self.head.next
                self._remove_node(lru)
                del self.cache[lru.key]

            new_node = Node(key, value)
            self._add_to_end(new_node)
            self.cache[key] = new_node
```