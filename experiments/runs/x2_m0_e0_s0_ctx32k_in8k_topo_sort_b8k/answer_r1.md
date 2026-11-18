### 구현 설명
카안(Kahn) 알고리즘에 최소 힙(`heapq`)을 결합하여 구현합니다.
1. `deps`의 키와 값에 등장하는 모든 노드를 수집해 진입 차수(`in_degree`)를 0으로 초기화합니다.
2. 의존 관계 `p -> node`를 따라 `in_degree[node]`를 증가시키고, 후속 노드 목록(`dependents[p]`)을 기록합니다.
3. 진입 차수가 0인 노드를 최소 힙에 담습니다. Python의 `heapq`는 문자열 비교 시 사전순으로 가장 작은 값을 먼저 꺼내므로 출력 순서가Deterministically 결정됩니다.
4. 힙에서 노드를 하나씩 꺼내 결과 리스트에 추가하고, 해당 노드에 의존하는 후속 노드들의 진입 차수를 감소시킵니다. 새 진입 차수가 0이 된 노드는 힙에 삽입합니다.
5. 알고리즘 종료 시 결과 리스트의 길이가 전체 고유 노드의 개수와 다르면 순환(cycle)이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq
from collections import defaultdict

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 고유 노드 수집 (키 및 목록에 등장하는 노드 포함)
    nodes = set(deps.keys())
    for prereqs in deps.values():
        nodes.update(prereqs)

    # 2. 진입 차수(in-degree) 및 후속 노드(dependents) 그래프 구성
    in_degree = {node: 0 for node in nodes}
    dependents = defaultdict(set)

    for node, prereqs in deps.items():
        for p in set(prereqs):  # 중복 제거로 정확한 진입 차수 계산
            in_degree[node] += 1
            dependents[p].add(node)

    # 3. 진입 차수가 0인 노드를 최소 힙에 저장 (사전순 보장)
    heap = [n for n in nodes if in_degree[n] == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in dependents[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 4. 순환 검사: 결과의 길이가 전체 노드 수보다 작으면 사이클 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")

    return result
```