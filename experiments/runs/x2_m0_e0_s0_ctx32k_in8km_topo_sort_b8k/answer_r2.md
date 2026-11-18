### 구현 설명
1. **노드 수집**: `deps`의 키(종속받는 노드)와 값들(선행 노드 목록)을 합쳐 모든 등장 노드를 집합으로 관리합니다.
2. **그래프 구성**: 의존 관계(`x`가 `y`에 의존 → `y` 먼저 실행)를 역방향 인접 리스트(`predecessor → successor`)로 변환하고, 각 노드의 진입차수(in-degree)를 계산합니다.
3. **사전순 위상 정렬(Kahn's Algorithm)**: 진입차수가 `0`인 노드를 최소 힙(`heapq`)에 넣어 항상 사전순으로 가장 작은 순서부터 꺼냅니다. 꺼낸 노드의 후행 노드들의 진입차수를 감소시키고, `0`이 되는 순간 힙에 다시 추가합니다.
4. **사이클 감지**: 처리된 결과 노드 수가 총 등장 노드 수보다 적으면 사이클 존재를 의미하므로 `ValueError`를 발생시킵니다.

### 최종 코드
```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 1. 모든 등장 노드 수집 (키 + 의존 목록에 포함된 값)
    all_nodes = set(deps.keys())
    for predecessors in deps.values():
        all_nodes.update(predecessors)

    # 2. 인접 리스트 및 진입차수(in-degree) 초기화
    adj = {node: [] for node in all_nodes}
    in_degree = {node: 0 for node in all_nodes}

    for node, predecessors in deps.items():
        for pred in predecessors:
            adj[pred].append(node)
            in_degree[node] += 1

    # 3. 진입차수가 0인 노드를 사전순 정렬을 위해 최소 힙에 삽입
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

    # 4. 결과 길이가 총 노드 수와 다르면 사이클 존재
    if len(result) != len(all_nodes):
        raise ValueError("의존성 그래프에 사이클이 존재합니다.")

    return result
```