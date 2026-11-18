이 함수는 **캐인(Kahn) 알고리즘**에 최소 힙(min-heap)을 결합하여 구현합니다. 

1. 키와 값에 등장하는 모든 노드를 수집하고, 의존 관계의 역방향 그래프(`adj`) 및 진입차수(`indegree`)를 계산합니다.
2. 진입차수가 `0`인 노드를 최소 힙에 넣습니다. Python의 `heapq`는 문자열 비교 시 사전순(lexicographical)을 자동으로 보장합니다.
3. 힙에서 작은 순서대로 노드를 꺼내 결과에 추가하고, 그 노드에 의존하는 후행 노드들의 진입차수를 감소시킵니다. 진입차수가 `0`이 되면 다시 힙에 삽입합니다.
4. 최종 처리된 노드의 수가 전체 노드 수보다 적으면 순환(cycle)이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 키와 값에 등장하는 모든 고유 노드 수집
    all_nodes = set(deps.keys())
    for prereqs in deps.values():
        all_nodes.update(prereqs)
        
    # 진입차수 계산 및 역방향 인접 리스트 구성 (의존 관계: p -> node)
    indegree = {node: 0 for node in all_nodes}
    adj = {node: [] for node in all_nodes}
    
    for node, prereqs in deps.items():
        for p in prereqs:
            adj[p].append(node)
            indegree[node] += 1
            
    # 진입차수가 0인 노드를 최소 힙에 초기화 (사전순 우선 보장)
    heap = [node for node in all_nodes if indegree[node] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(heap, v)
                
    # 처리된 노드 수가 전체 수보다 적으면 순환이 존재함
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected in dependencies")
        
    return result
```