`LRUCache`는 **해시맵 + 양방향 연결리스트** 조합으로 구현합니다.
- 해시맵(`dict`)은 키를 O(1)에 탐색하고 노드를 참조합니다.
- 양방향 연결리스트는 사용 순서를 유지하며, 헤드 쪽이 최근 사용, 테일 쪽이 가장 오래된 항목을 가리킵니다.
- `get` 시 해당 노드를 헤드로 이동시키고, `put` 시 존재하면 값을 갱신 후 헤드로 이동, 없으면 생성 후 헤드에 추가합니다. 용량을 초과하면 테일 직전 노드를 제거합니다.
-capacity 0`인 경우 즉시 반환/무시하도록 처리합니다.

```python
class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be >= 0")
        self.capacity = capacity
        self.cache: dict[int, Node] = {}
        
        # 더미 헤드/테일로 경계 조건 처리 단순화
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node) -> None:
        """노드를 헤드 직후에 삽입"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """연결리스트에서 노드 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: Node) -> None:
        """노드를 연결리스트 앞에서 재배치 (get 또는 기존 key put 시 사용)"""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node:
        """테일 직전 노드 제거 및 반환"""
        node = self.tail.prev
        self._remove_node(node)