해시맵(`dict`)과 더블 링크드 리스트를 결합하여 구현합니다. 딕셔너리는 O(1) 평균 시간 내에 키 조회 및 노드 접근을 담당하고, 더블 링크드 리스트는 사용 순서를 관리합니다(리스트 시작 부분: 최신 사용 / 끝 부분: 최오래 사용).

- `get`: 키가 있으면 해당 노드를 리스트 맨 앞으로 이동(O(1))해 ‘최신 사용’으로 갱신하고 값을 반환합니다. 없으면 `-1`을 반환합니다.
- `put`: 기존 키면 값을 업데이트 후 맨 앞으로 이동합니다. 새 키면 용량(`len(cache) == capacity`) 초과 시 꼬리(`tail.prev`)에 있는 LRU 노드를 제거한 뒤, 새 노드를 맨 앞에 삽입합니다.
- 더미 `head`/`tail` 노드를 사용하면 빈 리스트나 단일 노드 처리 시 별도의 경계 체크가 필요 없습니다.
- `capacity <= 0`인 경우 `put`에서 즉시 반환하여 메모리를 낭비하지 않도록 합니다.

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
        self.cache = {}
        
        # 더미 헤드 & 테일 노드 (인서트/리무브 시 경계 조건 제거)
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node) -> None:
        # 헤드 바로 뒤에 삽입 (최신 사용 위치)
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def _remove_node(self, node: Node) -> None:
        # 특정 노드를 링크드 리스트에서 분리
        pr, nx = node.prev, node.next
        pr.next = nx
        nx.prev = pr

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove_node(node)
        self._add_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
        else:
            if len(self.cache) == self.capacity:
                lru = self.tail.prev
                del self.cache[lru.key]
                self._remove_node(lru)
                
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
```