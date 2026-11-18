### 구현 요약
LRU Cache는 **해시맵(딕셔너리)**과 **더블 링크드 리스트**를 결합하여 표준적으로 구현합니다.
- 해시맵(`self.cache`)은 키에 대한 `O(1)` 조회와 노드 직접 참조를 담당합니다.
- 더블 링크드 리스트는 사용 순서(MRU → LRU)를 유지하며, 더미 헤드(선두)와 더미 테일(후미)을 두어 삽입/삭제 경계 조건 처리를 간소화합니다.
- `capacity <= 0`인 경우 초기 단계에서 즉시 반환하거나 무시하여 "저장하지 않는다"는 요구사항을 충족합니다.
- 모든 연산은 해시 조회와 링크드 리스트 포인터 재할당만으로 구성되므로 평균 `O(1)` 시간 복잡도를 가집니다.

```python
class Node:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None

class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("capacity must be >= 0")
        
        self.capacity = capacity
        self.cache: dict[int, Node] = {}
        
        # 더미 노드: 선두(MRU 기준), 후미(LRU 기준)에 위치해 경계 조건 처리를 간소화
        self.dummy_head = Node()
        self.dummy_tail = Node()
        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.prev = self.dummy_head

    def _add_to_head(self, node: Node) -> None:
        """더미 헤드 바로 뒤에 노드 삽입 (MRU 위치로 이동)."""
        node.prev = self.dummy_head
        node.next = self.dummy_head.next
        self.dummy_head.next.prev = node
        self.dummy_head.next = node

    def _remove_node(self, node: Node) -> None:
        """리스트에서 해당 노드 물리적으로 제거."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: Node) -> None:
        """노드를 선두로 이동 (최신 사용 기록으로 갱신)."""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> Node:
        """더미 테일 바로 앞 노드 제거 및 반환 (LRU 대상)."""
        tail_node = self.dummy_tail.prev
        self._remove_node(tail_node)
        return tail_node

    def get(self, key: int) -> int:
        if self.capacity <= 0:
            return -1
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)  # 조회 시 최신 사용 기록으로 갱신
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)  # 갱신 시 최신 사용 기록으로 이동
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)  # 선두에 추가
            
            # 용량 초과 시 가장 오래된 키(LRU) 제거
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]
```