### 핵심 설계
- **해시맵(`dict`)** + **더블 리링크드 리스트** 조합으로 구현합니다.
- 해시맵은 키를 O(1)로 탐색하고 노드 참조를 저장합니다.
- 더블 리링크드 리스트는 사용 순서를 관리하며, 더미 `head`(가장 최근)와 `tail`(Least Recently Used)을 둬서 경계 조건 처리를 단순화합니다.
- `get` 시 조회한 노드를 리스트 맨 앞으로 이동시킵니다.
- `put` 시 키가 존재하면 값을 갱신하고 맨 앞으로 이동합니다. 없으면 새 노드를 추가 후, 용량 초과 시 `tail.prev`(가장 오래된 키)를 제거합니다.
- `capacity == 0` 일 경우 `put` 에서 즉시 반환해 저장하지 않도록 처리합니다.
- 모든 연산이 해시 탐색 및 포인터 재연결만으로 이루어져 평균 **O(1)** 시간 복잡도를 보장합니다.

```python
class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        
        # 더미 헤드(가장 최근 사용)와 테일(LRU 위치)
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_front(self, node: Node) -> None:
        """노드를 head 바로 뒤(가장 최근)에 삽입"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """리스트에서 노드를 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)      # 현재 위치 제거
            self._add_to_front(node)     # 맨 앞으로 이동 (최근 사용)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_front(node)
        else:
            # 용량 초과 시 LRU(테일 바로 앞) 제거
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self._remove_node(lru)
                del self.cache[lru.key]

            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
```