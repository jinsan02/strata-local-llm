LRU Cache는 `O(1)` 시간 복잡도를 만족하기 위해 **해시맵(dict) + 양방향 연결리스트**를 결합하여 구현합니다.
- **해시맵**: 키로 노드를 즉시 찾거나 삭제/삽입할 때 사용 (`O(1)`)
- **양방향 연결리스트**: 사용 순서를 관리합니다. 리스트 끝(더미 Tail 앞)이 가장 최근 사용, 머리(더미 Head 뒤)가 가장 오래된 사용 위치입니다. 포인터 재배열만으로 이동/삭제 (`O(1)`)

용량이 0인 경우 즉시 반환하도록 처리하며, 표준 라이브러리는 `functools.lru_cache`만 제외하고 자유롭게 사용합니다.

```python
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        
        # 더미 Head & Tail로 경계 조건 제거
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_end(self, node: Node):
        """연결리스트 맨 끝(Tail 직전)에 노드 삽입"""
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def _remove(self, node: Node):
        """연결리스트에서 특정 노드 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove(node)
        self._add_to_end(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        if key in self.cache:
            # 기존 키: 값 갱신 & 최근 사용 위치로 이동
            node = self.cache