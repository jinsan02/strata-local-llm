이 문제는 **진입차수 기반 위상 정렬(Kahn's Algorithm)**에 **최소 힙(min-heap)**을 결합하면 자연스럽게 해결됩니다.
- `deps[x]`의 원소는 `x`로 향하는 간선(`pred → x`)을 의미합니다.
- 진입차수가 0인 노드만 우선순위 큐(힙)에 넣고, 가장 작은 문자열부터 추출하면 사전순 유일 정렬이 자동으로 보장됩니다.
- 결과 리스트 길이가 전체 노드 수보다 작으면 사이클 존재를 의미하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 노드 수집 (키와 값 목록 모두)
    all_nodes = set(deps.keys())
    for preds in deps.values():
        all_nodes.update(preds)
        
    # 2. 그래프 구성 및 진입차수 계산
    adj = defaultdict(set)
    for node, preds in deps.items():
        for pred in preds:
            adj[pred].add(node)  # 중복 간선 제거
            
    in_degree = {node: 0 for node in all_nodes}
    for u in adj:
        for v in adj[u]:
            in_degree[v] += 1
             
    # 3. 진입차수 0인 노드를 사전순으로 관리하기 위해 최소 힙에 초기화
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
                
    # 4. 사이클 체크 및 반환
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
    return result
```