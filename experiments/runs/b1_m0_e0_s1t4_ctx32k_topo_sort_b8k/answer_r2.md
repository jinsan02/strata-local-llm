Kahn 알고리즘을 활용합니다. 진입차수(`in_degree`)가 `0`인 노드를 최소 힙(min-heap)에 저장하여 추출할 때마다 사전순 정렬을 자동으로 보장합니다. 그래프를 순회하며 의존성을 해제하고, 최종적으로 방문한 노드 수가 총 고유 노드 수보다 적으면 순환이 존재한다고 판단해 `ValueError`를 발생시킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 모든 고유 노드 수집 (키와 값에 모두 포함)
    nodes = set(deps.keys())
    for prereqs in deps.values():
        nodes.update(prereqs)

    # 순방향 그래프 및 진입차수 초기화
    adj = {n: [] for n in nodes}
    in_degree = {n: 0 for n in nodes}

    for node, prereqs in deps.items():
        for p in set(prereqs):  # 중복 의존 제거
            adj[p].append(node)
            in_degree[node] += 1

    # 진입차수 0인 노드를 최소 힙에 저장 (사전순 추출 보장)
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

    # 결과 길이가 총 노드 수보다 작으면 순환 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")

    return result
```