```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set()
    adj = defaultdict(list)
    in_degree = defaultdict(int)

    # 그래프 구성 및 모든 노드 수집
    for x, prereqs in deps.items():
        nodes.add(x)
        for p in prereqs:
            nodes.add(p)
            adj[p].append(x)
            in_degree[x] += 1

    # 진입차수 0인 노드를 최소 힙에 초기화 (사전순 정렬 보장)
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

    # 처리된 노드 수가 전체 노드 수와 다르면 순환 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")

    return result
```