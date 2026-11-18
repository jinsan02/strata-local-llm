`deps[x]`는 `x`보다 먼저 방문해야 하는 선행 노드 목록이므로, 방향은 `선행 → 현재` 입니다. 사전순 tie-breaking을 위해 **최소 힙(min-heap)**을 사용하는 카한(Kahn) 알고리즘으로 구현하면 됩니다.

1. 모든 등장 노드를 수집하고 진입차수(in-degree)와 인접 리스트를 구성합니다.
2. 진입차수가 `0`인 노드를 최소 힙에 넣고, 힙에서 사전순으로 가장 작은 값을 하나씩 꺼내 정렬 결과에 추가합니다.
3. 꺼낸 노드의 후속 노드들의 진입차수를 감소시키고, `0`이 되면 힙에 삽입합니다.
4. 결과 리스트의 길이가 전체 노드 수보다 적으면 순환이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 노드 수집 및 진입차수 초기화
    nodes = set(deps.keys())
    for lst in deps.values():
        nodes.update(lst)
    
    in_degree = {node: 0 for node in nodes}
    adj = defaultdict(list)
    
    # 2. 그래프 및 진입차수 구성 (선행 -> 후속 방향)
    for target, sources in deps.items():
        for source in sources:
            adj[source].append(target)
            in_degree[target] += 1
            
    # 3. 진입차수 0인 노드를 사전순 최소 힙에 삽입
    heap = [n for n in nodes if in_degree[n] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        node = heapq.heappop(heap)
        result.append(node)
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, neighbor)
                
    # 4. 순환 검사
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in dependencies.")
        
    return result
```