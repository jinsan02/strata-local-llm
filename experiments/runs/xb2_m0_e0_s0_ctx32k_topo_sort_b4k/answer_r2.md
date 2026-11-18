이 문제는 **Kahn 알고리즘**에 최소 힙(`heapq`)을 결합해 구현합니다.

1. `deps`의 키와 값에 등장하는 노드를 모두 수집하고, 진입 차수(in-degree)를 계산합니다.
2. 진입 차수가 `0`인 노드를 최소 힙에 저장합니다. 힙은 사전순 비교를 자동 지원하므로 동시 실행 가능한 노드 중 가장 작은 것을 항상 먼저 꺼냅니다.
3. 힙에서 노드를 꺼내 결과 리스트에 추가하고, 해당 노드가 의존하는 후속 노드의 진입 차수를 1 감소시킵니다. 차수가 `0`이 되면 힙에 삽입합니다.
4. 처리된 노드 수가 전체 노드 수보다 적으면 순환(cycle) 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 모든 등장 노드 수집
    nodes = set(deps.keys())
    for prereqs in deps.values():
        nodes.update(prereqs)
        
    # 진입 차수 및 인접 리스트 구성 (prerequisite -> dependent)
    in_degree = {node: 0 for node in nodes}
    adj = defaultdict(list)
    
    for node, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(node)
            in_degree[node] += 1
            
    # 진입 차수 0인 노드를 사전순 우선 힙에 초기화
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
                
    # 순환 확인
    if len(result) != len(nodes):
        raise ValueError("Cycle detected in dependencies.")
        
    return result
```