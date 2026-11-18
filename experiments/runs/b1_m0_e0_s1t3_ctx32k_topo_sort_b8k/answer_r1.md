**설명**: 
에이커스(Kahn) 알고리즘을 사용합니다. 먼저 모든 노드의 진입차수(in-degree)를 계산한 후, 진입차수가 `0`인 노드를 최소 힙(min-heap)에 삽입합니다. 힙에서 사전순으로 가장 작은 노드를 하나씩 꺼내 결과 리스트에 추가하고, 해당 노드와 연결된 후행 노드의 진입차수를 감소시킵니다. 다시 진입차수가 `0`이 되면 힙에 넣습니다. 최종적으로 처리된 노드의 개수가 전체 고유 노드 수보다 작으면 사이클이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 모든 고유 노드 수집 (키와 값 모두 포함)
    all_nodes = set(deps.keys())
    for lst in deps.values():
        all_nodes.update(lst)

    # 인접 리스트 및 진입차수 초기화
    adj = {node: [] for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}

    # 그래프 구성 (의존 방향: dep -> x)
    for x, pre_list in deps.items():
        for dep in set(pre_list):  # 중복 간선 방지
            adj[dep].append(x)
            in_degree[x] += 1

    # 진입차수가 0인 노드를 최소 힙에 저장 (사전순 tie-breaking 보장)
    heap = [n for n in all_nodes if in_degree[n] == 0]
    heapq.heapify(heap)

    res = []
    while heap:
        u = heapq.heappop(heap)
        res.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 처리된 노드 수가 전체 수와 다르면 사이클 존재
    if len(res) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return res
```