### 핵심 동작 원리
1. **그래프 구성**: `deps[x]`의 요소들은 `x`보다 앞에 와야 하므로, 의존성 방향을 역전시켜 `p -> u` (사전 조건 `p` → 대상 `u`) 로 전향 연결 관계를 집합(`set`)으로 저장합니다. 중복 간선을 자동으로 제거하여 진입차수 계산이 정확해집니다.
2. **진입차수(in-degree) 초기화**: 모든 노드의 진입차수를 0으로 설정한 뒤, 그래프의 간선 수만큼 대상 노드의 진입차수를 증가시킵니다.
3. **사전순 정렬 보장 (Kahn's Algorithm + Min-Heap)**: 진입차수가 `0`인 노드를 최소 힙(`heapq`)에 쌓습니다. 힙은 문자열 기준 사전순으로 가장 작은 값을 상단에 유지하므로, 동시에 처리 가능한 노드가 여러 개면 항상 사전순 최솟값을 먼저 꺼냅니다.
4. **사이클 감지**: 결과 리스트의 길이가 전체 고유 노드 수와 다르면 순환 의존이 존재함을 의미하며 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    adj = defaultdict(set)
    nodes = set(deps.keys())
    
    # 의존성 방향 역전 및 모든 노드 수집 (p -> u)
    for u, prereqs in deps.items():
        for p in prereqs:
            nodes.add(p)
            adj[p].add(u)
            
    # 진입차수 계산
    in_degree = {node: 0 for node in nodes}
    for p in adj:
        for u in adj[p]:
            in_degree[u] += 1
            
    # 진입차수가 0인 노드만 힙에 초기화 (사전순 우선 처리)
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
                
    # 사이클 존재 여부 확인
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
        
    return result
```