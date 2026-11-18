### 설명
1. **노드 수집 & 그래프 구성**: `deps`의 키와 값에 등장하는 모든 문자열을 집합으로 모은 뒤, 역방향 간선(`의존 노드 → 대상 노드`)과 인차수(`in_degree`)를 계산합니다. 키에 없는 값-only 노드는 인차수가 0이므로 자동으로 큐/힙에 진입합니다.
2. **사전순 위상 정렬 (Kahn's Algorithm + Min-Heap)**: 인차수가 0인 노드를 `heapq`에 담고, 항상 사전순 최솟값을 꺼냅니다. 해당 노드를 처리할 때 후속 노드의 인차수를 감소시켜 0이 되면 다시 힙에 삽입합니다. 이 방식으로 동시 실행 가능한 여러 노드 중 사전순 첫 번째가 고정적으로 선택됩니다.
3. **순환 감지**: 반복 종료 후 결과 리스트의 크기가 전체 노드 수보다 작으면 사이클이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 노드 수집 (키 + 값에 등장하는 전체)
    all_nodes = set(deps.keys())
    for lst in deps.values():
        all_nodes.update(lst)
        
    # 2. 인차수 초기화 및 역방향 간선(의존 -> 대상) 구축
    in_degree = {node: 0 for node in all_nodes}
    graph = defaultdict(list)
    
    for target, prerequisites in deps.items():
        in_degree[target] = len(prerequisites)
        for prev in prerequisites:
            graph[prev].append(target)
            
    # 3. 인차수가 0인 노드를 사전순 정렬을 위해 최소힙에 저장
    heap = [node for node in all_nodes if in_degree[node] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)
                
    # 4. 사이클 감지
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
```