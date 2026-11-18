**핵심 아이디어**
1. **그래프 구성**: `deps[x]`는 `x`보다 앞에 와야 하는 노드이므로, 간선을 `prereq → x` 방향으로 잡고 진입차수(in-degree)를 계산합니다. 키에 없는 노드도 `set`으로 수집해 포함시킵니다.
2. **위상 정렬 + 최소 힙**: 진입차수가 0인 노드를 `heapq`에 넣고, 매 단계마다 사전순으로 가장 작은(node)를 pop합니다. 이를 통해 동시 배치 가능한 노드 중 순서 규칙을 자연스럽게 따릅니다.
3. **순환 감지**: 최종 결과 리스트의 길이가 전체 노드 수와 다르면 방문하지 못한 노드가 있음을 의미하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 노드 수집 (키에 없는 노드도 포함)
    nodes = set(deps.keys())
    for prereqs in deps.values():
        nodes.update(prereqs)

    graph = defaultdict(list)
    in_degree = {node: 0 for node in nodes}

    # 2. 그래프 및 진입차수 계산 (prereq -> x 방향)
    for x, prereqs in deps.items():
        for p in prereqs:
            graph[p].append(x)
            in_degree[x] += 1

    # 3. 진입차수가 0인 노드를 최소 힙에 삽입
    heap = [node for node in nodes if in_degree[node] == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)       # 사전순으로 가장 작은 노드 선택
        result.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 4. 순환 감지
    if len(result) != len(nodes):
        raise ValueError("순환이 존재합니다.")

    return result
```