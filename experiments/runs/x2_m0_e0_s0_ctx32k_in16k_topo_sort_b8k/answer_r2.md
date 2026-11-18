### 설명
카알(Kahn) 알고리즘에 최소 힙(`heapq`)을 결합해 구현합니다. 모든 노드의 진입차수(in-degree)를 계산한 뒤, 진입차수가 `0`인 노드들을 힙에 넣습니다. 힙은 사전순 정렬을 보장하므로 `heappop()` 할 때마다 동적으로 놓을 수 있는 노드 중 가장 작은 것부터 확정됩니다. 처리 과정에서 의존하는 노드의 진입차수를 감소시켜 `0`이 되면 다시 힙에 넣고, 최종 결과의 길이가 전체 노드 수보다 작으면 순환(cycle)이 있음을 의미해 `ValueError`를 일으킵니다.

### 코드
```python
import heapq
from typing import Dict, List

def topo_sort(deps: Dict[str, List[str]]) -> List[str]]:
    # 1. 모든 노드 수집 (키 + 값에 나오는 모든 문자열)
    nodes = set(deps.keys())
    for prereqs in deps.values():
        nodes.update(prereqs)

    # 2. 진입차수 및 인접 리스트 초기화
    in_degree = {node: 0 for node in nodes}
    adj = {node: [] for node in nodes]
    
    for x, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(x)      # p -> x 방향 간선
            in_degree[x] += 1     # x의 진입차수 증가

    # 3. 진입차수가 0인 노드를 최소 힙에 저장 (사전순 정렬 보장)
    heap = [node for node in nodes if in_degree[node] == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)   # 사전순으로 가장 작은 노드 선택
        result.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 4. 순환 검출: 모든 노드를 결과에 담지 못했으면 사이클 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
    
    return result
```