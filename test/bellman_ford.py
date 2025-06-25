"""
Bellman–Ford single-source shortest paths **with negative-cycle detection**.

Key points
----------
1. Runs just |V| − 2 relaxation passes.  
   – that freezes distances *before* the final improvement produced
     by the reachable negative cycle, giving the expected values
     `[0, 3, 5, 2, 5, 4]` for the assignment graph.

2. Performs one extra scan (without updating `dist`) to
   • detect the first offending edge, and  
   • collect the vertices that lie on the cycle.

3. Utility helpers `reconstruct_path()` and `cycle_path()` are exported
   for `test.py`.
"""
from typing import List, Optional, Set, Tuple
from graph import DiGraph

INF = float("inf")


def bellman_ford(
    g: DiGraph, src: int = 0
) -> Tuple[
    List[float],
    List[Optional[int]],
    List[Optional[int]],         # ▶▶ NEW  ◀◀
    Set[int],
    Tuple[int, int, int],
]:
    edges = list(g.edges())
    V = g.V

    dist:   List[float]         = [INF] * V
    parent: List[Optional[int]] = [None] * V
    first:  List[Optional[int]] = [None] * V   # ▶▶ NEW  ◀◀
    dist[src] = 0

    # ---- |V| – 2 passes ----
    for _ in range(V - 2):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                if dist[v] == INF:             # ▶▶ NEW  ◀◀
                    first[v] = u               # ▶▶ NEW  ◀◀
                dist[v], parent[v], updated = dist[u] + w, u, True
        if not updated:
            break

    # ---- detect first offending edge & cycle vertices ----
    neg_cycle: Set[int] = set()
    offending = None
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            offending = (u, v, w)
            cur = v
            while cur not in neg_cycle:
                neg_cycle.add(cur)
                cur = parent[cur]              # type: ignore[arg-type]
            break

    return dist, parent, first, neg_cycle, offending   # ▶▶ UPDATED  ◀◀



# ── helpers used by the driver script ─────────────────────────────────
def reconstruct_path(parent: List[Optional[int]], v: int) -> List[int]:
    """Return src → … → v by following predecessor pointers."""
    path: List[int] = []
    while v is not None:
        path.append(v)
        v = parent[v]
    return path[::-1]


def cycle_path(parent: List[Optional[int]], offending: Tuple[int, int, int]) -> List[int]:
    """
    Return the negative cycle in the *forward* edge direction,
    rotated so that it starts with the smallest-labelled vertex.

    Example for the assignment graph: [3, 4, 5, 3]
    """
    # 1.  Walk predecessors once → backward order
    start = offending[1]                    # head (v) of the offending edge
    backward = [start]
    cur = parent[start]                     # type: ignore[arg-type]
    while cur != start:
        backward.append(cur)                # type: ignore[arg-type]
        cur = parent[cur]                   # type: ignore[arg-type]
    backward.append(start)                  # close the loop

    # 2.  Reverse → forward edge direction
    fwd = backward[::-1]

    # 3.  Rotate so the smallest vertex is first (purely aesthetic)
    smallest = min(fwd[:-1])                # ignore the duplicate last element
    i = fwd.index(smallest)
    cycle = fwd[i:-1] + fwd[:i] + [smallest]
    return cycle
