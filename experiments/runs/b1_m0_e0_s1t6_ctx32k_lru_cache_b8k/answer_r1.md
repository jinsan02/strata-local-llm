### 핵심 설계
- **해시 맵(`dict`)** + **더블 링크드 리스트(DLL)** 조합이 표준 해법입니다. 해시는 키를 `O(1)`에 찾고, DLL은 노드의 삽입/삭제를 `O(1)`로 처리하며 사용 순서를 유지합니다.
- 더미 `head`(최신 사용)와 `tail`(가장 오래된 사용)를 두어 경계 조건(null 체크)을 제거합니다.
- `get`에서 키를 찾으면 해당 노드를 DLL의 맨 앞(`head`)으로 이동시켜 가장 최근 사용으로 갱신합니다.
- `put`에서 새 키 삽입 또는 기존 키 갱신 후 머리로 이동시키고, 용량(`capacity`) 초과 시 꼬리(`tail`) 바로 앞의 노드(LRU)를 제거합니다.
- `capacity == 0`이면 즉시 `-1` 또는 리턴하여 인스턴스 공간을 거의 차지하지 않습니다.

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
        self.cache = {}  # key -> Node
        
        # 더미 머리(MRU 기준 앞)와 꼬리(LRU 기준 끝)
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: Node) -> None:
        """노드를 head 바로 뒤에 삽입"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """DLL에서 노드 제거"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node: Node) -> None:
        """노드를 제거하고 head 바로 뒤에 삽입"""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """tail 바로 앞(LRU 노드)을 제거하고 반환"""
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key: int) -> int:
        if self.capacity == 0:
            return -1
        
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
            
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)
            
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]
```