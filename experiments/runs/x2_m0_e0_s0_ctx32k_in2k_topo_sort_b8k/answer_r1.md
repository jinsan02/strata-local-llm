### 접근 방식
1. **노드 수집**: `deps`의 키와 모든 값 목록을 합쳐 전체 노드 집합(`all_nodes`)을 만듭니다.
2. **진입차수 계산 & 인접 리스트 구성**: `p → x` 방향 간선으로 그래프를 구축하고, 각 노드의 진입차수(in-degree)를 기록합니다.
3. **Kahn 알고리즘 + 최소 힙**: 진입차수가 0인 노드들을 `heapq`에 넣어 항상 사전순으로 가장 작은 것을 먼저 처리합니다. 노드를 처리할 때마다 대상 노드의 진입차수를 감소시키고, 0이 되면 힙에 추가합니다.
4. **순환 감지**: 최종 결과 리스트의 길이가 전체 노드 수보다 작으면 사이클이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 키와 값 목록에 등장하는 모든 노드 수집
    all_nodes = set(deps.keys())
    for preds in deps.values():
        all_nodes.update(preds)

    in_degree = {node: 0 for node in all_nodes}
    adj = defaultdict(list)

    # 진입차수 계산 및 인접 리스트 구성 (p -> x 방향)
    for x, preds in deps.items():
        for p in preds:
            adj[p].append(x)
            in_degree[x] += 1

    # 진입차수가 0인 노드를 최소 힙에 저장하여 사전순 우선 보장
    heap = [node for node, deg in in_degree.items() if deg == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 처리된 노드 수가 전체 노드 수와 다르면 사이클 존재
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
    return result
```