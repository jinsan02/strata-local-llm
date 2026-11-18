이 함수는 **카한 알고리즘(Kahn's Algorithm)**을 기반으로 하며, 충돌 시 사전순으로 작은 노드를 우선 처리하기 위해 `heapq`(최소 힙)를 사용합니다. 전체 등장 노드의 진입차수(in-degree)를 계산한 후 0인 노드를 힙에 넣습니다. 매번 힙에서 최솟값을 꺼내 결과에 추가하고, 해당 노드와 연결된后继 노드의 진입차수를 감소시킵니다. 감소 후 진입차수가 0이 되면 다시 힙에 삽입합니다. 최종적으로 처리된 노드 수가 전체 고유 노드 수보다 적으면 사이클이 존재하므로 `ValueError`를 발생시킵니다.

```python
import heapq

def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    all_nodes = set(deps.keys())
    for preds in deps.values():
        all_nodes.update(preds)
        
    in_degree = {node: 0 for node in all_nodes}
    adj = {node: [] for node in all_nodes}
    
    for node, preds in deps.items():
        for pred in preds:
            adj[pred].append(node)
            in_degree[node] += 1
            
    heap = [node for node in all_nodes if in_degree[node] == 0]
    heapq.heapify(heap)
    
    result = []
    while heap:
        curr = heapq.heappop(heap)
        result.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, neighbor)
                
    if len(result) != len(all_nodes):
        raise ValueError("Cycle detected")
        
    return result
```