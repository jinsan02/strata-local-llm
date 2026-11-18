### 구현 요약
1. `deps`의 키와 값(목록)을 모두 합쳐 **전체 노드 집합**을 만든다.
2. 각 노드의 진입 차수(`in_degree`)와 인접 리스트(`adj`)를 구축한다. `deps[x]`의 원소 `p`는 `x`의 선행 조건이므로 간선 `p → x`를 추가한다.
3. 진입 차수가 0인 노드를 **최소 힙(min-heap)**에 넣고 정렬 후 꺼낸다. 이를 통해 동시에 배치 가능한 노드 중 사전순 최소를 항상 우선 선택한다.
4. 노드를 처리할 때마다 연결된 후속 노드의 진입 차수를 감소시키고, 0이 되면 힙에 추가한다.
5. 결과 리스트의 길이가 전체 노드 수보다 작으면 순환(cycle)이 존재하므로 `ValueError`를 발생시킨다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 모든 노드 수집 (키 + 값 목록에 등장하는 노드)
    all_nodes = set(deps.keys())
    for lst in deps.values():
        all_nodes.update(lst)
        
    in_degree = {node: 0 for node in all_nodes}
    adj = {node: [] for node in all_nodes}
    
    # 진입 차수 및 인접 리스트 구축
    for x, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(x)
            in_degree[x] += 1
            
    # 진입 차수가 0인 노드를 사전순 정렬을 보장하는 힙에 삽입
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
        raise ValueError("Cycle detected")
        
    return result
```