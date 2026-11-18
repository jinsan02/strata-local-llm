### 설명
Kahn's 알고리즘을 기반으로 구현합니다. 진입 차수(`in_degree`)가 `0`인 노드를 최소 힙(`heapq`)에 담아 꺼내면, 동적으로 놓을 수 있는 노드 중 **사전순으로 가장 작은 것**이 항상 먼저 처리되어 결과가 단 하나의 정렬로 확정됩니다. 모든 노드가 결과 리스트에 포함되지 않으면 순환 구조가 존재하므로 `ValueError`를 발생시킵니다.

### 코드
```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]]:
    # 키와 값에 등장하는 모든 고유 노드 수집
    all_nodes = set(deps.keys()) | {n for prereqs in deps.values() for n in prereqs}
    
    # 인접 리스트 및 진입 차수(in-degree) 초기화
    adj = defaultdict(set)
    in_degree = {n: 0 for n in all_nodes}
    
    for node, prereqs in deps.items():
        for p in prereqs]:
            if node not in adj[p]:
                adj[p].add(node]
                in_degree[node] += 1
                
    # 진입 차수가 0인 노드를 최소 힙에 담아 사전순 처리 보장
    heap = [n for n in all_nodes if in_degree[n] == 0]]
    heapq.heapify(heap)]
    
    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)]
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)]
                
    # 처리되지 않은 노드가 남으면 순환(cycle)이 존재함
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
```