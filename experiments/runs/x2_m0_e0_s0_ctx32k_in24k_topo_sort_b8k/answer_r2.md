위상 정렬(Kahn's Algorithm)과 최소 힙(min-heap)을 결합한 해결책입니다.

1. **그래프 구성**: `deps[x]`는 `x`의 선행 노드이므로, 각 선행 노드에서 `x`를 향하는 전향(edge) 간선을 만듭니다.
2. **입력차(in-degree)**: 각 노드의 진입 차수를 계산합니다. 입력 리스트에 중복이 있을 수 있으므로 집합으로 변환하여 정확히 카운트합니다.
3. **사전순 보장**: 진입 차수가 `0`인 노드만 힙에 담고, `heapq`를 사용해 항상 사전순 가장 작은 노드를 먼저 꺼냅니다. 이를 통해 동시에 배치 가능한 경우마다 결정론적인 순서를 고정합니다.
4. **순환 감지**: 최종 결과 길이가 전체 고유 노드 수와 다르면 사이클이 존재하므로 `ValueError`를 발생합니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 키와 값에 등장하는 모든 고유 노드 수집
    all_nodes = set(deps.keys()) | {node for ns in deps.values() for node in ns}
    
    # 전향 간선 그래프 및 진입차수 초기화
    adj = {node: set() for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}
    
    for key, preds in deps.items():
        for pred in set(preds):          # 중복 선행 노드 제거
            adj[pred].add(key)
            in_degree[key] += 1

    # 진입차수가 0인 노드를 사전순으로 처리하기 위해 최소 힙 사용
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
        raise ValueError("Graph contains a cycle")
        
    return result
```