위상 정렬의 **Kahn 알고리즘**에 `heapq`(우선순위 큐)를 결합하면 됩니다. 진입차수(`in_degree`)가 0인 노드들을 최소 힙에 담아 항상 사전순으로 가장 작은 노드를 먼저 처리하면 Deterministic한 결과를 얻을 수 있고, 최종 방문 노드 수가 총 노드 수와 다르면 순환이 감지되어 `ValueError`를 일으킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 노드 수집 (키 + 값에 등장하는 노드)
    all_nodes = set(deps.keys())
    for prereqs in deps.values():
        all_nodes.update(prereqs)

    # 2. 그래프 구성 (역방향 deps를 정방향 간선으로 변환)
    adj = {node: [] for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}
    
    for u, prereqs in deps.items():
        # 중복 의존성 방지
        for p in set(prereqs):
            adj[p].append(u)
            in_degree[u] += 1

    # 3. 진입차수가 0인 노드를 최소 힙에 초기화 (사전순 보장)
    heap = [node for node in all_nodes if in_degree[node] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 4. 사이클 감지
    if len(order) != len(all_nodes):
        raise ValueError("Cycle detected in dependencies")
        
    return order
```