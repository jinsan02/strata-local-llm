### 설명
1. **그래프 구성**: `deps[x]`는 `x`보다 먼저 와야 하는 노드이므로, 간선은 `의존노드 → x` 방향으로 생성합니다. 키에 포함되지 않은 노드도 `adj`와 `deg`에 동적으로 추가합니다.
2. **진입차수(in-degree)**: 각 노드에 들어오는 간선 수를 세어 `deg` 딕셔너리에 저장합니다. 진입차수가 0인 노드부터 처리할 수 있습니다.
3. **사전순 확정**: 동시 처리 가능한 노드가 여러 개일 때 결과의 순서를 단일하게 고정하기 위해 최소 힙(`heapq`)을 사용합니다. 힙은 문자열을 사전순으로 정렬하여 항상 가장 작은 값을 먼저 꺼냅니다.
4. **사이클 감지**: 위상 정렬이 완료되면 결과 리스트의 길이가 총 노드 수와 같아야 합니다. 그렇지 않으면 처리되지 않은 노드가 남아 사이클이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 인접 리스트 및 진입차수 초기화 (목록에만 등장하는 노드도 포함)
    adj = {node: [] for node in deps}
    deg = {node: 0 for node in deps}
    
    for node, dependents in deps.items():
        for dep in dependents:
            if dep not in adj:
                adj[dep] = []
                deg[dep] = 0
            adj[dep].append(node)   # dep → node 방향 간선 생성
            deg[node] += 1
            
    # 진입차수가 0인 노드를 최소 힙에 초기화 (사전순 정렬 보장)
    heap = [node for node in deg if deg[node] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in adj[u]:
            deg[v] -= 1
            if deg[v] == 0:
                heapq.heappush(heap, v)
                
    # 처리된 노드 수와 총 노드 수가 다르면 사이클 존재
    if len(result) != len(deg):
        raise ValueError("순환이 있는 의존성 그래프입니다.")
        
    return result
```