Kahn의 알고리즘(Kahn's Algorithm)에 최소 힙(`heapq`)을 결합하면 진입 차수가 0인 노드 중 사전순으로 가장 작은 것을 매 단계마다 선택할 수 있어 결과의 순서가 단 하나만 보장됩니다. 모든 키와 값에 등장하는 노드를 수집한 뒤 그래프를 구성하고, 방문한 노드 수가 전체 고유 노드수와 다르면 사이클 존재로 간주하여 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    """의존 관계 그래프에 대한 위상 정렬. 동시 배치 가능 노드 중 사전순 최소를 우선."""
    # 1. 키와 목록 모두에서 고유 노드 수집
    nodes = set(deps.keys())
    for children in deps.values():
        nodes.update(children)
        
    in_degree = {node: 0 for node in nodes}
    adj = defaultdict(list)
    
    # 2. 방향 그래프 및 진입 차수(in-degree) 계산 (부모 u -> 자식 v)
    for v, parents in deps.items():
        for u in parents:
            adj[u].append(v)
            in_degree[v] += 1
            
    # 3. 진입 차수가 0인 노드를 최소 힙에 추가 (사전순 결정용)
    pq = [u for u in nodes if in_degree[u] == 0]
    heapq.heapify(pq)
    
    result = []
    while pq:
        u = heapq.heappop(pq)
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(pq, v)
                
    # 4. 사이클 감지
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
    return result
```