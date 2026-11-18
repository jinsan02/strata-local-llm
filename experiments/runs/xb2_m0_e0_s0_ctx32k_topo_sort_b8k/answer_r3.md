진입차수(in-degree) 기반의 **카혼(Kahn) 알고리즘**에 최소 힙(min-heap)을 결합한 구현입니다. 진입차수가 0인 노드를 힙에 담아 `heappop` 할 때 항상 사전순으로 가장 작은 노드가 먼저 선택되도록 하며, 처리되지 않은 노드가 남아있으면 순환으로 판단해 `ValueError`를 발생시킵니다.

```python
import heapq
from typing import Dict, List

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 키와 값에 등장하는 모든 노드 수집
    nodes = set(deps.keys())
    for preds in deps.values():
        nodes.update(preds)

    # 2. 인접 리스트(선행자 -> 후속자) 및 진입차수 계산
    adj = {n: [] for n in nodes}
    in_degree = {n: 0 for n in nodes}
    
    for u, preds in deps.items():
        unique_preds = set(preds)
        for p in unique_preds:
            adj[p].append(u)
        in_degree[u] += len(unique_preds)

    # 3. 진입차수가 0인 노드를 최소 힙에 저장 (사전순 보장)
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

    # 4. 모든 노드가 처리되지 않으면 순환 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
        
    return result
```