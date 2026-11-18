### 간단한 설계 설명
해당 요구사항을 평균 `O(1)` 시간 복잡도로 해결하기 위해 **해시맵(`dict`)**과 **더미(Dummy) 헤드/테일이 있는 이중 연결 리스트**를 조합합니다.

- **해시맵**: 키를 `O(1)` 만에 탐색하고 해당 노드 참조를 관리합니다.
- **이중 연결 리스트**: 사용 순서를 유지합니다. 가장 최근에 사용한 노드는 head 바로 뒤에 위치하며, 가장 오래 사용하지 않은(LRU) 노드는 tail 바로 앞에 위치합니다. 더미 노드를 사용하여 경계 조건 처리를 단순화합니다.
- `get`: 키가 존재하면 해당 노드를 찾아 list의 head 앞으로 이동(접근 시간 최신화) 후 값을 반환합니다. 없으면 `-1`을 반환합니다.
- `put`: capacity 가 0 이면 즉시 리턴합니다. 기존 키라면 값을 갱신하고 head 로 이동합니다. 새 키라면 노드를 새로 생성해 head 앞에 추가하고 맵에 등록합니다. 이때 저장된 키 개수가 capacity 를 초과하면 tail 바로 앞의 LRU 노드를 리스트와 맵에서 제거합니다.

```python
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = max(0, capacity)
        self.cache = {}
        
        # 더미 헤드/테일 노드 초기화 (경계 조건 처리 간소화)
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_head(self, node: Node) -> None:
        """노드를 헤드의 바로 다음 위치에 삽입합니다 (가장 최근 사용)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """연결 리스트에서 특정 노드를 물리적으로 제거합니다."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node) -> None:
        """기존 노드를 삭제한 뒤, 헤드의 바로 다음에 재삽입합니다."""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node:
        """테일의 바로 앞(LRU 노드)을 제거하고 반환합니다."""
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)  # 최신 사용으로 순서 갱신
            return node.value
        return -1

    def put(self, key, value) -> None:
        # capacity가 0이면 아예 저장하지 않음
        if self.capacity <= 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)  # 갱신 시 최신 사용으로 이동
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)  # 새 노드는 head 앞에 추가
            
            # 용량 초과 시 가장 오래 사용하지 않은 노드(LRU) 삭제
            if len(self.cache) > self.capacity:
                tail_node = self._pop_tail()
                del self.cache[tail_node.key]
```