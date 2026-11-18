### 설명
1. **그래프 구성**: `deps[x]`는 `x`의 선행 노드들이므로, 간선 방향은 `선행 -> x`로 잡고 후속 노드 목록(`successors`)과 진입 차수(`in_degree`)를 계산합니다.
2. **노드 수집**: 키와 값에 등장한 모든 노드를 집합으로 모아 초기화합니다.
3. **동적 정렬**: 진입 차수가 `0`인 노드를 최소 힙(`heapq`)에 담습니다. 힙에서 가장 작은(사전순) 노드를 꺼내 결과에 추가하고, 해당 노드의 후속 노드 진입 차수를 줄입니다. 차수가 `0`이 되면 힙에 삽입하여 항상 사전순 최적 선택을 보장합니다.
4. **순환 감지**: 처리된 노드 수가 총 노드 수보다 적으면 사이클 존재. 이때 `ValueError`를 발생시킵니다.

### 코드
```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 노드 수집 (키 + 값에 등장하는 노드)
    all_nodes = set(deps.keys())
    for preds in deps.values():
        all_nodes.update(preds)
        
    # 2. 후속 관계 및 진입 차수 초기화
    successors = {n: [] for n in all_nodes}
    in_degree = {n: 0 for n in all_nodes}
    
    for node, preds in deps.items():
        for pred in preds:
            successors[pred].append(node)
            in_degree[node] += 1
            
    # 3. 진입 차수 0인 노드를 사전순으로 처리할 최소 힙 준비
    pq = [n for n in all_nodes if in_degree[n] == 0]
    heapq.heapify(pq)
    
    result = []
    while pq:
        u = heapq.heappop(pq)  # 사전순 가장 작은 노드 선택
        result.append(u)
        
        for v in successors[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(pq, v)
                
    # 4. 사이클 체크
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
```