### 설명
**Kahn의 알고리즘**에 최소 힙(`heapq`)을 결합하면 진입 차수가 0인 노드 중 사전순으로 가장 작은 것을 자동으로 선택할 수 있어 결과가 완전히 결정됩니다. 
1. 키와 값 목록에서 모든 고유 노드를 수집하고 진입 차수(in-degree) 및 인접 리스트를 초기화합니다.
2. 의존성 방향(`prereq → node`)으로 그래프를 구성하며, 각 노드의 진입 차수를 계산합니다.
3. 진입 차수가 0인 노드를 최소 힙에 넣고, 힙에서 하나씩 꺼내며 연결된 후속 노드의 진입 차수를 감소시킵니다. 0이 되면 다시 힙에 넣습니다.
4. 최종 결과 길이가 전체 고유 노드 수보다 작으면 사이클 존재 → `ValueError` 발생.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    all_nodes = set(deps.keys())
    for prereqs in deps.values():
        all_nodes.update(prereqs)

    in_degree = {node: 0 for node in all_nodes}
    adj = {node: [] for node in all_nodes}

    for node, prereqs in deps.items():
        seen = set()
        for p in prereqs:
            if p not in seen:
                seen.add(p)
                in_degree[node] += 1
                adj[p].append(node)

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
        raise ValueError("Cycle detected in dependencies")

    return result
```