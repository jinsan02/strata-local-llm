### 설명
1. **노드 수집**: 딕셔너리의 키와 값에出现的된 모든 문자열을 집합 `all_nodes`에 저장해 의존성 그래프의 전체 정점을 정의합니다.
2. **그래프 구성**: `deps[x]`에 있는 원소 `p`는 `x`보다 먼저 처리해야 하므로, 간선 방향은 `p → x`입니다. 인접 리스트 `adj`와 진입차수 `in_degree`를 계산하며, 중복 간선이 반복 계산을 유발하지 않도록 집합으로 관리합니다.
3. **위상 정렬 (Kahn's Algorithm + Heap)**: 진입차수가 0인 노드를 최소 힙에 삽입합니다. 매 순간 힙에서 사전순으로 가장 작은 노드를 꺼내 결과에 추가하고, 해당 노드와 연결된 후속 노드의 진입차수를 감소시켜 0이 되면 다시 힙에 넣습니다.
4. **순환 감지**: 최종 결과 리스트의 길이가 전체 노드 수보다 작으면 의존성 사이클이 존재함을 의미하며, 이 경우 `ValueError`를 발생시킵니다.

### 코드
```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 키와 값에 등장하는 모든 노드를 수집
    all_nodes = set(deps.keys())
    for prereqs in deps.values():
        all_nodes.update(prereqs)
        
    # 2. 진입차수 및 인접 리스트 구성 (간선 방향: prerequisite → dependent)
    in_degree = {node: 0 for node in all_nodes}
    adj = {node: set() for node in all_nodes}
    
    for x, prereqs in deps.items():
        for p in prereqs:
            if x not in adj[p]:
                adj[p].add(x)
                in_degree[x] += 1
                
    # 3. 진입차수가 0인 노드를 최소 힙에 초기화
    heap = [node for node in all_nodes if in_degree[node] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)
                
    # 4. 사이클 검증
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
```