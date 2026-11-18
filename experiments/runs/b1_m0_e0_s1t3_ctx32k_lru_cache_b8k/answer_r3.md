### 설계 설명
- **데이터 구조**: 해시맵(`dict`)과 이중 연결 리스트(`Doubly Linked List`)를 결합합니다.
  - 해시맵은 키를 `O(1)`에 탐색하고 해당 노드를 바로 참조하는 데 사용합니다.
  - 이중 연결 리스트는 사용 순서를 관리합니다. 더미 `head`(LRU 쪽)와 `tail`(MRU 쪽)을 두어 삽입/삭제 경계를统一합니다.
- **`get(key)`**: 키가 없으면 `-1` 반환. 있으면 노드를 리스트에서 제거 후 `tail` 직전에 재삽입해 최신 순서로 갱신하고 값을 반환합니다.
- **`put(key, value)`**: 
  - 용량(`capacity`)이 `0`이면 즉시 반환합니다.
  - 키가 기존에 있으면 값을 업데이트한 뒤 노드를 `tail` 쪽으로 이동합니다.
  - 키가 없으면 새 노드를 생성해 캐시에 추가하고 `tail` 직전에 삽입합니다. 이후 저장된 키 수(`len(cache)`)가 용량을 넘으면 `head`의 다음 노드(Least Recently Used)를 제거하고 해시맵에서도 삭제합니다.
- **시간 복잡도**: 모든 연산이 상수 시간 `O(1)`입니다.

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        
        # 더미 헤드(LRU)와 테일(MRU) 노드
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_tail(self, node: Node) -> None:
        """노드를 tail 직전에 추가 (최신 사용 순서로 이동)"""
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node

    def _remove_node(self, node: Node) -> None:
        """노드를 현재 위치에서 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove_node(node)
        self._add_to_tail(node)
        return node.val

    def put(self, key, value) -> None:
        if self.capacity == 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove_node(node)
            self._add_to_tail(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_tail(new_node)
            
            # 용량 초과 시 LRU 노드 제거
            if len(self.cache) > self.capacity:
                lru = self.head.next
                self._remove_node(lru)
                del self.cache[lru.key]
```