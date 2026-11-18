### 핵심 구현 논리
1. **그래프 구성**: `deps`에서 각 의존 관계 `p → x` (`p`가 `x`보다 먼저 와야 함)를 인접 리스트로 변환하고, 각 노드의 진입차수(`in_degree`)를 계산합니다.
2. **최소 힙 활용**: 진입차수가 `0`인 노드를 최소 힙(min-heap)에 담습니다. 힙은 자동으로 사전순(lexicographical order)으로 가장 작은 값을 꺼내므로, 동시에 처리 가능한 경우 요구사항을 만족합니다.
3. **카한(Kahn) 알고리즘 반복**: 힙에서 노드를 하나씩 꺼내 결과 리스트에 추가하고, 해당 노드와 연결된 후속 노드의 진입차수를 감소시킵니다. 만약 감소 후 진입차수가 `0`이 되면 힙에 삽입합니다.
4. **사이클 감지**: 알고리즘 종료 시 결과 리스트의 길이가 전체 고유 노드 수와 다르면 순환 구조가 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 고유 노드 수집 (키 + 값에 등장하는 모두)
    all_nodes = set(deps.keys())
    for prereqs in deps.values():
        all_nodes.update(prereqs)

    # 2. 진입차수 및 인접 리스트 초기화
    in_degree = {node: 0 for node in all_nodes}
    graph = defaultdict(list)

    for node, prereqs in deps.items():
        for p in set(prereqs):  # 중복 의존 관계로 인한 진입차수 과계산 방지
            graph[p].append(node)
            in_degree[node] += 1

    # 3. 진입차수가 0인 노드를 최소 힙에 삽입 (사전순 정렬 보장)
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