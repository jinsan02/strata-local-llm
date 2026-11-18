### 핵심 로직 설명
- **카한 알고리즘(Kahn's Algorithm)** 기반 진입차수(in-degree) 위상 정렬을 사용합니다.
- `deps`의 키(종속 대상)와 값(선행 조건)을 모두 수집해 전체 노드 집합을 만듭니다.
- 진입차수가 0인 노드를 **최소 힙(min-heap)**에 담아 사전순으로 가장 작은 문자열을 먼저 꺼내 처리합니다.
- 결과 리스트의 길이가 전체 노드 수보다 작으면 사이클이 존재함을 의미하므로 `ValueError`를 발생시킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 키와 값에 등장하는 모든 노드 수집
    all_nodes = set(deps.keys())
    for prereqs in deps.values():
        all_nodes.update(prereqs)
        
    # 2. 인접 리스트 및 진입차수(in-degree) 초기화
    adj = {node: [] for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}
    
    for node, prereqs in deps.items():
        seen = set()
        for p in prereqs:
            if p not in seen:  # 중복 의존성 방지
                adj[p].append(node)
                in_degree[node] += 1
                seen.add(p)
                
    # 3. 진입차수 0인 노드를 최소 힙에 삽입 (사전순 정렬 자동 보장)
    heap = [n for n in all_nodes if in_degree[n] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        curr = heapq.heappop(heap)
        result.append(curr)
        
        for nxt in adj[curr]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                heapq.heappush(heap, nxt)
                
    # 4. 사이클 검출 및 반환
    if len(result) != len(all_nodes):
        raise ValueError("의존성 순환이 감지되었습니다.")
        
    return result
```