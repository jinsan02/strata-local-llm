Kahn's 알고리즘에 `heapq` (최소 힙)를 결합하면 됩니다.
1. 모든 노드를 수집하고 진입차수(`in_degree`)와 인접 리스트(`adj`)를 구성합니다.
2. 진입차수가 0인 노드를 최소 힙에 담습니다. 힙은 자동으로 사전순 가장 작은 노드를 우선 추출합니다.
3. 힙에서 노드를 꺼내 결과에 추가하고, 해당 노드가 의존하는 후속 노드의 진입차수를 감소시킵니다. 감소한 값이 0이 되면 힙에 삽입합니다.
4. 최종 결과의 노드 수가 전체 노드 수와 다르면 순환이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 키와 값에 등장하는 모든 노드 수집
    all_nodes = set(deps.keys()) | {p for preds in deps.values() for p in preds}
    
    # 그래프 구성 (인접 리스트 & 진입차수)
    adj = {n: [] for n in all_nodes}
    in_degree = {n: 0 for n in all_nodes}
    
    for x, preds in deps.items():
        for p in set(preds):  # 중복 의존 제거로 진입차수 정확히 계산
            adj[p].append(x)
            in_degree[x] += 1
            
    # 진입차수가 0인 노드를 사전순 정렬을 위한 최소 힙에 초기화
    heap = [n for n, d in in_degree.items() if d == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)
                
    # 결과 노드 수가 전체 노드 수보다 적으면 순환(cycle) 존재
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
```