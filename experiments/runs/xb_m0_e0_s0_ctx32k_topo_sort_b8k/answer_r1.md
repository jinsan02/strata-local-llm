### 핵심 로직
1. **노드 수집**: 키(`target`)와 값(`prereq`)에 등장하는 모든 노드를 집합으로 추출해 결측 노드를 방지합니다.
2. **그래프 구성 & 진입차수**: `prereq → target` 방향으로 간선을 생성하고, 각 노드의 진입차수(`in_degree`)를 계산합니다. 중복 간선은 `set`을 이용해 자연스럽게 제거됩니다.
3. **최소 힙 우선순위 처리**: 진입차수가 `0`인 노드를 `heapq`에 넣습니다. 항상 `heappop`으로 사전순으로 가장 작은 노드를 먼저 꺼내므로 tie-breaking 조건이 자동으로 충족됩니다.
4. **위상 정렬 & 순환 감지**: 힙에서 노드를 제거하며 연결된 노드의 진입차수를 감소시킵니다. 모든 노드를 방문했는지 길이 비교로 확인하고, 불일치 시 `ValueError`를 발생시킵니다.

### 코드
```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 등장하는 모든 노드 수집 (키 + 값에 등장)
    nodes = set(deps.keys())
    for prereqs in deps.values():
        nodes.update(prereqs)

    # 2. 인접 리스트 및 진입차수 초기화
    adj = defaultdict(set)
    in_degree = {node: 0 for node in nodes}
    
    for target, prereqs in deps.items():
        for p in prereqs:
            adj[p].add(target)      # p -> target 방향 간선
            in_degree[target] += 1

    # 3. 진입차수가 0인 노드를 사전순 정렬을 위한 최소 힙에 담기
    heap = [node for node in nodes if in_degree[node] == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 4. 순환 감지
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
        
    return result
```