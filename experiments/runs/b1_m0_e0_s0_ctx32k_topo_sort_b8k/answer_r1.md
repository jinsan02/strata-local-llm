### 설명
카힌(Kahn) 알고리즘에 **최소 힙(min-heap)**을 결합합니다. 진입차수(in-degree)가 0인 노드를 `heapq`에 보관하면 매 반복마다 사전순으로 가장 작은 노드가 자동으로 선택됩니다. 모든 처리가 끝난 후 결과 리스트의 길이가 전체 고유 노드 수보다 작으면 사이클이 존재하는 것이므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 키와 값에 등장하는 모든 고유 노드 추출
    nodes = set(deps.keys()) | {p for prereqs in deps.values() for p in prereqs}
    
    adj = defaultdict(list)
    in_degree = {node: 0 for node in nodes}
    
    # 역방향 그래프 구성 및 진입차수 계산
    for x, prereqs in deps.items():
        seen = set()
        for p in prereqs:
            if p not in seen:
                seen.add(p)
                adj[p].append(x)      # p -> x 간선 추가
                in_degree[x] += 1     # x의 진입차수 증가
                
    # 진입차수가 0인 노드를 최소 힙에 초기화 (사전순 정렬 보장)
    heap = [node for node in nodes if in_degree[node] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        curr = heapq.heappop(heap)
        result.append(curr)
        
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, neighbor)
                
    # 사이클 감지: 처리된 노드 수가 전체 고유 노드 수보다 적으면 불가능
    if len(result) < len(nodes):
        raise ValueError("Cycle detected")
        
    return result
```