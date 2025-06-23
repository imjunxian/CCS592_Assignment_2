"""
Bellman–Ford single-source shortest path with negative-cycle detection.
Returns (dist, parent, neg_cycle_vertices).
"""

from typing import List, Tuple, Set

INF = float("inf")

def extract_negative_cycle(parent, start):
        cycle = [start]
        cur = parent[start]
        while cur != start:
            cycle.append(cur)
            cur = parent[cur]
        cycle.append(start)  # complete the cycle
        cycle.reverse()
        return cycle

def bellman_ford(n: int, edges, src: int = 0) -> Tuple[List[float], List[int], Set[int]]:
    # ------------------------------------------------------------------
    # If `edges` is a generator (e.g. g.edges()), materialise it so we
    # can iterate multiple times (|V|−1 relaxations + 1 cycle check).
    # ------------------------------------------------------------------
    edges = list(edges)

    dist: List[float] = [INF] * n
    parent: List[int] = [-1] * n
    dist[src] = 0

    # |V| − 1 relaxation rounds
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:  # early exit on convergence
            break

    # extra pass ⇒ improvement ⇒ negative cycle reachable from src
    neg_vertices: Set[int] = set()
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            # back-walk n steps to ensure we're inside the cycle
            cur = v
            for _ in range(n):
                cur = parent[cur]
            start = cur
            while True:
                neg_vertices.add(cur)
                cur = parent[cur]
                if cur == start:
                    break
                            # back-walk n steps to ensure we're inside the cycle
            cur = v
            for _ in range(n):
                cur = parent[cur]
            cycle = extract_negative_cycle(parent, cur)
            print("Negative cycle path:", cycle)
            neg_vertices.update(cycle)

    
                    
# ---------------------- Helper: Extract Negative Cycle ------------------------

    return dist, parent, neg_vertices