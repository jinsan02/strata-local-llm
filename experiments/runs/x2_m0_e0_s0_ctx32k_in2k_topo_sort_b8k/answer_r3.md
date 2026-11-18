### 알고리즘 개요
`deps[x]`는 `x`보다 앞에 와야 하는 전위(predecessor) 목록이므로, 각 의존 관계에 대해 방향 간선 `p → x`를 그립니다. 모든 노드(키와 값에 등장한 모두)의 진입차수(in-degree)를 계산한 후, 진입차수가 `0`인 노드를 **최소 힙(min-heap)**에 저장합니다. 
힙에서 사전순으로 가장 작은 노드를 꺼내 결과 리스트에 추가하고, 해당 노드가 연결된 후속 노드의 진입차수를 감소시킵니다. 진행 중 진입차수가 `0`이 되면 힙에 재삽입합니다. 이 과정을 반복하면 매 단계마다 선택 가능한 노드 중 사전순 최솟값을 먼저 뽑아 결정론적인 정렬 결과를 얻습니다. 최종 처리된 노드 수가 총 노드 수보다 적으면 사이클이 존재함을 의미하므로 `ValueError`를 던집니다. 시간복잡도는 `O(N log N + E)`입니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 키와 의존 목록에 등장한 모든 노드 수집
    nodes = set(deps.keys())
    for prereqs in deps.values():
        nodes.update(prereqs)

    # 그래프 구성 (간선: prerequisite → dependent) 및 진입차수 계산
    adj = {node: [] for node in nodes}
    in_degree = {node: 0 for node in nodes}
    
    for node, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(node)
            in_degree[node] += 1

    # 진입차수가 0인 노드를 사전순 최소 힙에 초기화
    heap = [node for node in nodes if in_degree[node] == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 처리된 노드 수가 총 노드 수와 다르면 사이클 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in dependencies.")
        
    return result
```