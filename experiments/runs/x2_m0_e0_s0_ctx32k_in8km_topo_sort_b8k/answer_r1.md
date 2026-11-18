위상 정렬을 위해 **커인(Kahn) 알고리즘**에 최소 힙(`heapq`)을 결합하면 됩니다.
1. 모든 노드의 진입차수(in-degree)를 계산하고, 진입차수가 0인 노드를 최소 힙에 넣습니다.
2. 힙에서 사전순으로 가장 작은 노드를 꺼내 결과에 추가합니다.
3. 해당 노드가 의존하는(다음에 오는) 노드들의 진입차수를 1 감소시키고, 0이 되면 힙에 재삽입합니다.
4. 반복 후 결과 리스트의 길이가 전체 고유 노드 수와 다르면 순환이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import deque

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 노드 수집 (키 + 목록에만出现的하는 종속 노드 포함)
    nodes = set(deps.keys())
    for prereqs in deps.values():
        nodes.update(prereqs)

    # 2. 진입차수 계산 및 인접 리스트 생성 (의존 관계: prereq -> dependant)
    in_degree = {node: 0 for node in nodes}
    adj = {node: [] for node in nodes}

    for node, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(node)
            in_degree[node] += 1

    # 3. 진입차수가 0인 노드를 최소 힙에 초기화 (사전순 보장)
    heap = [n for n, d in in_degree.items() if d == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 4. 사이클 감지
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in dependencies")
        
    return result
```