### 구현 요약
1. **노드 수집**: `deps`의 키와 모든 의존성 목록에 포함된 노드를 합쳐 전체 정점 집합을 만듭니다.
2. **그래프 구성**: 각 노드의 진입차수(`in_degree`)를 세우고, 의존 관계의 역방향(adj) 인접 리스트를 구축합니다. (의존원 → 현재노드 방향)
3. **사전순 확정**: 진입차수가 `0`인 노드를 `min-heap`에 저장합니다. 힙에서 최소값(사전순 가장 작은 노드)을 꺼내 결과에 추가하고, 그 노드가 의존하는 후속 노드의 진입차수를 감소시킵니다. 감소되어 `0`이 되는 노드는 다시 힙에 넣습니다.
4. **순환 검사**: 처리 후 결과 리스트의 크기가 전체 노드 수보다 작으면 사이클 존재 → `ValueError` 발생.

시간복잡도: `O(V log V + E)` (V: 노드 수, E: 의존 관계 수)

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 전체 노드 수집 (키 + 목록에 등장하는 모든 문자열)
    all_nodes = set(deps.keys())
    for prereqs in deps.values():
        all_nodes.update(prereqs)

    # 2. 진입차수(in-degree)와 역방향 간선(adjacency) 구성
    in_degree = {node: 0 for node in all_nodes}
    adj = defaultdict(list)

    for u, prereqs in deps.items():
        in_degree[u] += len(prereqs)
        for v in prereqs:
            adj[v].append(u)

    # 3. 진입차수 0인 노드를 최소힙에 담아 사전순으로 확정
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

    # 4. 사이클 검증
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected in dependencies")

    return result
```