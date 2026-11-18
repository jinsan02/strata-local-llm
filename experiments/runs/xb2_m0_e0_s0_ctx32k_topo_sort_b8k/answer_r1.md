### 설명
1. **그래프 구성**: 입력 딕셔너리 `deps`는 의존 관계(`prerequisite → target`)를 역방향으로 담고 있습니다. 이를 인접 리스트 `adj`와 진입차수(in-degree) 맵으로 변환합니다. 키와 값에 등장하는 모든 노드를 포함하도록 처리합니다.
2. **Kahn's Algorithm + Min-Heap**: 진입차수가 `0`인 노드를 최소 힙(min-heap)에 담습니다. 힙에서 사전순 가장 작은 노드를 꺼내 결과에 추가하고, 해당 노드의 후속 노드들의 진입차수를 감소시킵니다. 차수가 `0`이 되면 힙에 재삽입합니다. 이를 통해 매 단계 동시다발적으로 배치 가능한 노드 중 **가장 사전순 앞선 것**만 선택하게 되어 결과가 유일해집니다.
3. **순환 감지**: 알고리즘 종료 시 결과 리스트의 길이가 전체 노드 수와 다르면 순환이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 모든 등장 노드 수집
    all_nodes = set(deps.keys())
    for prereqs in deps.values():
        all_nodes.update(prereqs)

    # 진입차수 및 인접 리스트 초기화
    in_degree = {node: 0 for node in all_nodes}
    adj = {node: [] for node in all_nodes}
    
    for x, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(x)      # p -> x 간선
            in_degree[x] += 1     # x의 진입차수 증가

    # 진입차수가 0인 노드를 최소 힙에 초기화
    pq = [u for u in all_nodes if in_degree[u] == 0]
    heapq.heapify(pq)

    result = []
    while pq:
        u = heapq.heappop(pq)
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(pq, v)

    # 결과 길이가 전체 노드 수보다 작으면 순환 존재
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
```