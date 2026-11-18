```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 모든 노드 수집 (키와 값에 등장하는 노드 포함)
    nodes = set(deps.keys()) | {p for plist in deps.values() for p in plist}
    
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # 간선 및 진입차수 계산 (prereq -> x)
    for x, prereqs in deps.items():
        for p in prereqs:
            graph[p].append(x)
            in_degree[x] += 1
            
    # 진입차수가 0인 노드를 최소힙에 저장 (사전순 보장)
    heap = [node for node in nodes if in_degree[node] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)
                
    # 처리된 노드 수가 전체 노드 수와 다르면 순환 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
        
    return result
```