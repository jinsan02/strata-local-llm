### 설명
**카한(Kahn) 알고리즘**에 **최소힙(min-heap)**을 결합해 구현했습니다.
1. `deps`의 각 항목을 방향 그래프 간선(`pre → node`)으로 전환하며 진입차수(in-degree)와 인접 리스트를 구축합니다. 키에 없는 노드도 집합(`all_nodes`)에 추가해 누락 없이 포함시킵니다.
2. 진입차수가 `0`인 노드를 최소힙에 넣고, 힙에서 작은 값을 꺼내 결과에 추가합니다. 이때 이웃의 진입차수를 감소시켜 `0`이 되면 다시 힙에 넣습니다. 이를 통해 **동시에 선택 가능한 노드 중 사전순으로 가장 작은 것이 우선** 처리됩니다.
3. 완료 후 실제 반환된 노드 수가 전체 노드 수와 다르면 사이클이 존재함을 의미하므로 `ValueError`를 발생시킵니다.

### 코드
```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    in_degree = defaultdict(int)
    adj = defaultdict(list)
    all_nodes = set()

    for node, prereqs in deps.items():
        all_nodes.add(node)
        for pre in prereqs:
            all_nodes.add(pre)
            adj[pre].append(node)
            in_degree[node] += 1

    # 진입차수가 0인 노드 중 사전순 최소가 우선되도록 힙 사용
    heap = [n for n in all_nodes if in_degree[n] == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 사이클이 있으면 일부 노드만 처리됨
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected in dependencies")

    return result
```