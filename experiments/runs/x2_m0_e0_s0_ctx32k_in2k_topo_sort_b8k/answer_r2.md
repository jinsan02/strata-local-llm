이 작업은 **Kahn's Algorithm(진입차수 기반 위상 정렬)**에 `heapq`를 결합해 구현하면 됩니다.

1. 그래프의 모든 노드를 수집하고, 각 노드의 진입차수(in-degree)를 계산합니다.
2. 진입차수가 `0`인 노드들을 최소 힙(min-heap)에 넣습니다. 힙은 자동으로 사전순(lexicographical)으로 가장 작은 값을 우선 반환하므로 동시 대기 노드 중 하나를 정렬할 수 있습니다.
3. 힙에서 노드를 꺼내 결과에 추가하고, 해당 노드가 선행하는 후행 노드의 진입차수를 줄입니다. 새로운 진입차수 `0` 노드는 힙에 삽입합니다.
4. 결과 리스트의 크기가 전체 노드 수와 다르면 사이클이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict
from typing import Dict, List


def topo_sort(deps: Dict[str, List[str]]) -> List[str]:
    # 1. 그래프에 등장하는 모든 노드 수집
    nodes = set(deps.keys())
    for preds in deps.values():
        nodes.update(preds)

    # 2. 진입차수(in-degree) 계산 및 인접 리스트(adjacency) 구축
    in_degree = {node: 0 for node in nodes}
    graph = defaultdict(list)

    for node, preds in deps.items():
        for p in preds:
            in_degree[node] += 1      # node는 p가 먼저 와야 함 (진입차수 증가)
            graph[p].append(node)     # p 다음에 올 수 있는 노드 기록

    # 3. 진입차수가 0인 노드를 최소 힙에 초기화 (사전순 우선 정렬 보장)
    heap = [node for node in nodes if in_degree[node] == 0]
    heapq.heapify(heap)

    result: List[str] = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 4. 사이클 감지: 결과에 모든 노드가 포함되지 않았으면 순환 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in dependencies.")

    return result
```