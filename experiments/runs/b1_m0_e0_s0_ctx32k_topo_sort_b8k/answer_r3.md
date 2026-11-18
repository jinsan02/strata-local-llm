이 함수는 **카이언 알고리즘(Kahn's algorithm)**에 `heapq` 최소 힙을 결합해 구현합니다.

1. 모든 노드(키와 값 모두)를 수집하고, 의존 관계 역방향 그래프(`adj`)와 진입차(`in_degree`)를 계산합니다.
2. 진입차 `0`인 노드를 최소 힙에 삽입하여 **사전순으로 가장 작은 순서**대로 꺼내도록 합니다.
3. 노드를 처리할 때마다 후속 노드의 진입차를 감소시키고, `0`이 되면 힙에 추가합니다.
4. 결과 길이가 총 노드 수와 다르면 사이클 존재 → `ValueError` 발생.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 키와 값(선결조건) 모두를 집합으로 합쳐 모든 노드 수집
    nodes = set(deps.keys())
    for prereqs in deps.values():
        nodes.update(prereqs)

    # 역방향 그래프 및 진입차 초기화
    adj = {n: [] for n in nodes}
    in_degree = {n: 0 for n in nodes}

    for node, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(node)   # p -> node 의존 관계 저장
            in_degree[node] += 1

    # 진입차가 0인 노드를 최소 힙에 넣음 (사전순 정렬 보장)
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

    # 결과의 노드 수가 총 노드 수보다 적으면 사이클 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
        
    return result
```