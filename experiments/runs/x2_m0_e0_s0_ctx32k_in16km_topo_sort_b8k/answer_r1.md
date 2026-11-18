해당 과제는 **위상 정렬(Topological Sort)** 알고리즘을 구현하는 문제입니다. 요구사항을 만족하기 위해 `카한(Kahn) 알고리즘`에 `최소 힙(min-heap)`을 결합하면 됩니다.
1. 모든 키와 값(의존 노드)을 집합으로 수집해 전체 노드를 정의합니다.
2. 의존 방향(`p → node`)으로 인접 리스트를 만들고, 각 노드의 진입차수(in-degree)를 계산합니다.
3. 진입차수가 `0`인 노드를 최소 힙에 넣습니다. 힙은 사전순으로 가장 작은 값을 항상 맨 앞으로 뽑아주므로 deterministic ordering을 보장합니다.
4. 노드를 꺼낼 때마다 후행 노드의 진입차수를 줄이고, `0`이 되면 힙에 추가합니다.
5. 최종 결과 리스트의 길이가 전체 노드 수보다 작으면 순환(Cycle)이 있음을 의미하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 노드 수집 (키와 의존성 목록에 등장하는 노드 모두 포함)
    nodes = set(deps.keys())
    for preqs in deps.values():
        nodes.update(preqs)
        
    # 2. 인접 리스트 및 진입차수(in-degree) 계산
    adj = defaultdict(set)
    in_degree = {n: 0 for n in nodes}
    
    for node, preqs in deps.items():
        for p in preqs:
            adj[p].add(node)
            
    # 진입차수는 실제 고유 간선 수로 세야 함 (중복 의존성 방지)
    for u, vs in adj.items():
        for v in vs:
            in_degree[v] += 1
            
    # 3. 카한(Kahn) 알고리즘 + 최소 힙(사전순 결정)
    heap = [n for n in nodes if in_degree[n] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)
                
    # 4. 사이클 감지 (결과 길이가 전체 노드 수와 다르면 순환 존재)
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
        
    return result
```