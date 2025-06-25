"""
Binary-heap Dijkstra **with guard**:
raises ValueError (custom wording) when the graph contains a negative edge.
"""

import heapq
from typing import Dict, List, Tuple
from graph import DiGraph

INF = float("inf")


def _has_negative_edge(g: DiGraph) -> bool:
    return any(w < 0 for _, _, w in g.edges())


def dijkstra(g: DiGraph, src: int = 0) -> Tuple[List[float], Dict[int, int]]:
    if _has_negative_edge(g):
        raise ValueError("Negative edge detected – Dijkstra is invalid on this graph.")

    dist: List[float] = [INF] * g.V
    parent: Dict[int, int] = {src: -1}
    dist[src] = 0

    pq: List[Tuple[float, int]] = [(0, src)]  # (distance, vertex)

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:                      # stale entry
            continue
        for v, w in g.neighbours(u):
            if d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, parent
