# dijkstra.py
"""
Heap-based Dijkstra **with guard**:
raises ValueError if *any* edge weight is negative.
"""

import heapq
from typing import List, Tuple, Dict
from graph import DiGraph

INF = float("inf")


def _has_negative_edge(g: DiGraph) -> bool:
    return any(w < 0 for _, _, w in g.edges())


def dijkstra(g: DiGraph, src: int = 0) -> Tuple[List[float], Dict[int, int]]:
    """
    Dijkstra’s single-source shortest path.
    -----  WILL RAISE  -----
    ValueError  → graph contains a negative edge, so the algorithm is
                  not applicable.

    returns (dist, parent) if successful.
    """ 
    if _has_negative_edge(g):
        raise ValueError("Dijkstra requires all edge weights ≥ 0")

    dist: List[float] = [INF] * g.V
    parent: Dict[int, int] = {src: -1}
    dist[src] = 0

    pq: List[Tuple[float, int]] = [(0, src)]  # (distance, vertex)

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:          # stale queue entry
            continue
        for v, w in g.neighbours(u):
            if d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, parent
