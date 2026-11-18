`deps[x]`는 `x`보다 먼저 와야 하는 선행 노드이므로 `p → x` 방향으로 간선을 설정한다. 

1. 모든 노드(키와 값에 등장하는 문자열 전체)를 수집하고 진입차수(`in_degree`)를 0으로 초기화한 뒤, 의존 관계에 따라 진입차수를 업데이트한다.
2. 진입차수가 0인 노드를 `heapq`(min-heap)에 넣고, 매번 사전순이 가장 작은 노드를 꺼낸다 (Kahn’s algorithm 변형).
3. 꺼낸 노드의 후속 노드 진입차수를 줄이고 0이 되면 힙에 넣는다.
4. 결과 리스트 길이가 총 고유 노드 수보다 작으면 사이클 존재 → `ValueError` 발생.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    nodes = set(deps.keys())
    adj: dict[str, list[str]] = {}
    in_degree: dict[str, int] = {node: 0 for node in nodes}

    for x, prereqs in deps.items():
        for p in prereqs:
            nodes.add(p)
            adj.setdefault(p, []).append(x)
            in_degree[x] += 1

    # 목록에만 등장한 노드도 진입차수 사전에 추가
    for node in nodes:
        if node not in in_degree:
            in_degree[node] = 0

    heap = [node for node in nodes if in_degree[node] == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in adj.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    if len(result) != len(nodes):
        raise ValueError("Cycle detected")

    return result
```