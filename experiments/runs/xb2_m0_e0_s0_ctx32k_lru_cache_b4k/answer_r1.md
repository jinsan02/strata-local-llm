### 핵심 구현 방식
- **해시맵(`dict`) + 더블 리스 리스트** 조합으로 O(1) 조회/삽입/삭제를 보장합니다.
- 해시맵은 `key → Node` 매핑을 저장하여 빠른 탐색을 담당합니다.
- 가짜 `head`(최근 사용 끝) 와 `tail`(오래된 사용 시작) 를 감싸는 리스트로 순서를 관리합니다. 헤드 바로 뒤가 MRU, 테일 직전 노드가 LRU 입니다.
- `capacity == 0`인 경우 초기화 단계에서 즉시 종료하도록 분기 처리하여 메모리/연산 낭비를 방지합니다.

```python
class _Node:
    __slots__ = 'key', 'value', 'prev', 'next'
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        
        # 용량 0 이면 즉시 초기화 완료 (get/put 에서 별도 처리)
        if self.capacity == 0:
            return

        # 더블 리스 리스트: 가짜 헤드/테일 노드 생성 및 연결
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if self.capacity == 0 or key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)  # 사용 기록 갱신 (MRU 로 이동)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        if key in self.cache:
            # 기존 키 갱신 및 MRU 이동
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # 용량 초과 시 LRU(테일 직전) 삭제
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                del self.cache[lru.key]
                self._remove_node(lru)

            # 새 노드 생성 → 해시맵 저장 → 헤드 바로 뒤에 삽입
            new_node = _Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

    # --- 헬퍼 메소드 (모두 O(1)) ---
    def _add_to_head(self, node: _Node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: _Node):
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _move_to_head(self, node: _Node):
        self._remove_node(node)
        self._add_to_head(node)
```