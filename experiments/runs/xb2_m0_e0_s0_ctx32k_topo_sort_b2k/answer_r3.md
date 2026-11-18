**핵심 로직 설명**
1. **노드 및 간선 추출**: `deps`의 키와 값에 등장하는 모든 노드를 수집합니다. `y in deps[x]`는 `y → x` 방향의 간선을 의미하므로 인접 리스트로 변환하고 각 노드의 진입차수(`in_degree`)를 계산합니다.
2. **최소힙 기반 카한 알고리즘**: 진입차수가 0인 노드를 최소힙에 넣고, 힙에서 사전순으로 가장 작은 노드를 뽑아 정렬 결과에 추가합니다. 해당 노드와 연결된 후속 노드의 진입차수를 줄여 0이 되면 다시 힙에 넣습니다.
3. **순환 감지**: 최종 결과 리스트의 길이가 전체 노드 수보다 작다면 사이클이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 노드 수집
    all_nodes = set(deps.keys())
    for lst in deps.values():
        all_nodes.update(lst)
        
    # 2. 인접 리스트 및 진입차수 계산 (y → x 간선)
    in_degree = {node: 0 for node in all_nodes}
    adj = defaultdict(list)
    
    for x, preds in deps.items():
        for p in preds:
            adj[p].append(x)
            in_degree[x] += 1
            
    # 3. 진입차수 0인 노드 우선순위 큐 초기화
    heap = [node for node in all_nodes if in_degree[node] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)
                
    # 4. 사이클 존재 확인
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
```