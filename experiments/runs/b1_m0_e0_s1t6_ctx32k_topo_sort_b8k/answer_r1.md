### 핵심 접근법
1. **그래프 구성**: `deps[x]`에 있는 노드들은 `x`보다 먼저 오므로, 의존 방향을 역으로 잡아 `dep → x` 간선을 만들고 진입차수(`in_degree`)를 계산합니다.
2. **사전순 결정**: 동시에 처리 가능한 노드(진입차수 0) 중 가장 작은 문자열을 먼저 뽑기 위해 **최소 힙(min-heap)**을 사용합니다.
3. **순환 감지**: Kahn 알고리즘 기반으로 힙에서 꺼낸 노드의 총 개수가 전체 그래프의 고유 노드 수보다 적으면 순환이 존재함을 의미하며 이때 `ValueError`를 발생시킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    # 등장하는 모든 노드 수집 (키 또는 값에 모두 포함)
    nodes = set(deps.keys())
    for dep_list in deps.values():
        nodes.update(dep_list)

    # 인접 리스트 및 진입차수 초기화
    adj = {n: [] for n in nodes}
    in_degree = {n: 0 for n in nodes}

    # 의존 관계 역방향 간선 생성 (dep → x)
    for x, dep_list in deps.items():
        for dep in dep_list:
            adj[dep].append(x)
            in_degree[x] += 1

    # 진입차수가 0인 노드를 최소 힙에 저장 (사전순 정렬 보장)
    heap = [n for n in nodes if in_degree[n] == 0]
    heapq.heapify(heap)

    result = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    # 결과 길이가 전체 노드 수보다 작으면 순환 존재
    if len(result) != len(nodes):
        raise ValueError("Cycle detected")
        
    return result
```