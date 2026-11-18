### 설명
이 과제는 **Kahn's Algorithm**에 최소 힙(min-heap)을 결합한 위상 정렬입니다.
1. `deps`의 키와 값에 등장하는 모든 노드를 수집해 진입차수(`in_degree`)와 인접 리스트(`adj`)를 초기화합니다.
2. 진입차수가 `0`인 노드를 최소 힙에 넣고, 매 단계에서 사전순으로 가장 작은 노드를 꺼냅니다.
3. 해당 노드를 결과에 추가한 뒤, 의존하는 후속 노드들의 진입차수를 1 감소시킵니다. 감소해 `0`이 된 노드는 힙에 삽입합니다.
4. 모든 노드가 결과 리스트에 추가되면 완료됩니다. 최종 길이가 전체 노드 수보다 작으면 순환(`cycle`)이 존재하므로 `ValueError`를 발생시킵니다.

시간 복잡도: `O(V log V + E)` | 공간 복잡도: `O(V + E)`

### 최종 코드

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    all_nodes = set(deps.keys())
    for prereqs in deps.values():
        all_nodes.update(prereqs)

    in_degree = {node: 0 for node in all_nodes}
    adj = {node: [] for node in all_nodes}

    for node, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(node)
            in_degree[node] += 1

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

    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected in dependency graph")

    return result
```