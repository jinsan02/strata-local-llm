위상 정렬은 진입차수(in-degree)가 0인 노드부터 처리하는 **Kahn 알고리즘**을 사용한다. 사전순 우선 요구사항을 만족하기 위해 진입차수가 0인 노드들을 **최소 힙(min-heap)**에 저장하여 항상 알파벳 순으로 가장 작은 노드를 먼저 꺼내도록 한다. 모든 등장 노드(키 및 값)를 집합으로 수집해 그래프와 진입차수를 초기화하고, 정렬 결과의 길이가 전체 노드 수와 다르면 순환이 존재함을 감지해 `ValueError`를 발생시킨다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 키와 값에 등장하는 모든 노드 수집
    all_nodes = set(deps.keys()) | {n for lst in deps.values() for n in lst}
    
    # 인접 리스트 및 진입차수 초기화
    adj = {node: [] for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}
    
    for node, prereqs in deps.items():
        for pre in prereqs:
            adj[pre].append(node)      # pre -> node 간선 추가
            in_degree[node] += 1       # 진입차수 증가
            
    # 진입차수가 0인 노드를 최소 힙에 저장 (사전순 자동 정렬 보장)
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
                
    # 결과 길이가 총 노드 수보다 작으면 순환 존재
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
```