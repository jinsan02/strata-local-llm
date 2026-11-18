해시 테이블(`dict`)과 이중 연결 리스트를 결합하여 구현합니다. 해시 테이블은 키 기반 O(1) 조회를 담당하고, 연결 리스트는 접근 순서를 유지합니다. 더미(head/tail) 노드를 활용해 경계 조건 처리를 간소화했습니다.

- `get(key)`: 캐시에 있으면 해당 노드를 찾아 머리(dummy head) 바로 앞으로 이동(MRU 갱신) 후 값을 반환합니다. 없으면 -1 반환.
- `put(key, value)`: 키가 있으면 값을 갱신하고 헤드 앞으로 이동합니다. 없으면 새 노드를 생성해 캐시에 추가하고 헤드에 삽입한 후, `size > capacity`이면 꼬리(prev of tail)에 있는 LRU 노드를 제거합니다.
- `capacity <= 0`인 경우 `put`은 즉시 반환하며, `get`은 캐시가 항상 비어있으므로 -1을 반환합니다.

전체 연산이 해시 접근과 포인터 재할당으로만 이루어지므로 평균 **O(1)** 시간 복잡도를 보장합니다.

```python
class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = max(capacity, 0)
        self.cache: dict[int, Node] = {}
        self.size = 0
        
        # 더미 헤드(최신 사용)와 테일(오래된 사용) 노드
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node) -> None:
        """노드를 head 바로 뒤에 삽입"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """리스트에서 특정 노드 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: Node) -> None:
        """노드를 리스트 머리 바로 앞으로 이동"""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node | None:
        """테일 바로 앞(LRU) 노드를 제거하고 반환"""
        res = self.tail.prev
        if res is self.head:
            return None
        self._remove_node(res)
        return res

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)  # 접근 시 MRU로 이동
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
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
            lru_node = self._pop_tail()
            if lru_node is not None:
                del self.cache[lru_node.key]
                self.size -= 1
```