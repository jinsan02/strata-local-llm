### 설명
1. **그래프 구성**: `deps[x]`의 각 원소 `p`는 `x`보다 먼저 와야 하므로 방향 간선 `p → x`로 매핑합니다. `set`을 사용해 키와 모든 값(전달자 노드)을 포함하도록 전체 노드 집합을 구축합니다.
2. **진입차수 계산**: 각 노드가 진입하는 간선의 수(`indeg`)를 세고, 진입차수가 0인 노드를 최소 힙(`heapq`)에 넣습니다.
3. **사전순 고정**: 동시에 처리 가능한 노드 중 사전순으로 가장 작은 것을 먼저 꺼내므로 `heapq`(최소 힙)를 사용합니다. 힙에서 꺼낸 노드 `u`의 후속 노드 `v`의 진입차수를 줄이고, 0이 되면 힙에 삽입합니다.
4. **순환 감지**: 정렬이 끝난 후 결과 리스트 길이가 전체 노드 수보다 작으면 순환이 존재하므로 `ValueError`를 발생시킵니다.

### 코드
```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps)
    for prereqs in deps.values():
        nodes.update(prereqs)
        
    adj = defaultdict(list)
    indeg = {n: 0 for n in nodes}
    
    for x, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(x)
            indeg[x] += 1
            
    pq = [n for n in nodes if indeg[n] == 0]
    heapq.heapify(pq)
    
    result = []
    while pq:
        u = heapq.heappop(pq)
        result.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(pq, v)
                
    if len(result) != len(nodes):
        raise ValueError("순환이 감지되었습니다.")
    return result
```