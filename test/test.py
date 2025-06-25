# test.py
"""
▪ Builds the assignment graph.
▪ Bellman–Ford:
    – “Frozen” distances after |V|−2 passes
    – Final distances after |V|−1 passes
▪ Shows concrete paths for BOTH distance vectors:
    * frozen table  (cycle taken once)
    * final  table  (cycle taken twice)
▪ Attempts Dijkstra (and prints the guard error).
"""

from bellman_ford import bellman_ford, reconstruct_path, cycle_path
from dijkstra import dijkstra
from graph import DiGraph


# ── 1. Build the graph ──────────────────────────────────────────────
V = 6
E = [
    (0, 2, 5),
    (0, 1, 4),
    (2, 1, -2),
    (1, 3, 3),
    (3, 4, 2),
    (4, 5, -1),
    (5, 3, -2),
]
G = DiGraph.from_edges(V, E)

# ── 2. Frozen Bellman–Ford pass (|V|-2) ────────────────────────────
dist_frozen, parent, first_parent, neg_cycle, offending = bellman_ford(G, 0)
cycle = cycle_path(parent, offending)                # e.g. [3,4,5,3]
cycle_no_dup = cycle[:-1]
cycle_weight = sum(w for u, v, w in E if (u, v) in
                   list(zip(cycle_no_dup, cycle_no_dup[1:] + cycle_no_dup[:1])))


# ── 3. Final Bellman–Ford pass (|V|-1) ─────────────────────────────
def full_bellman_with_parent(g: DiGraph, src: int = 0):
    """ textbook |V|-1 passes, *also* return the parent pointers """
    INF = float("inf")
    dist = [INF] * g.V
    parent = [None] * g.V
    dist[src] = 0
    edges = list(g.edges())

    for _ in range(g.V - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v], parent[v] = dist[u] + w, u
    return dist, parent


dist_final, parent_final = full_bellman_with_parent(G, 0)


# ── 4. Helpers to build paths with N laps round the cycle ──────────
succ = {u: cycle_no_dup[(i + 1) % len(cycle_no_dup)]
        for i, u in enumerate(cycle_no_dup)}


def path_with_laps(v: int, laps: int) -> list[int]:
    """prefix to the cycle + 'laps' forward rounds of the cycle"""
    prefix = reconstruct_path(first_parent, v)
    # remove duplicate v at the end of prefix (if any)
    if prefix and prefix[-1] == v and v in neg_cycle:
        prefix.pop()

    path = prefix[:]
    cur = v
    for _ in range(laps):
        nxt = succ[cur]
        while nxt != v:
            path.append(nxt)
            cur, nxt = nxt, succ[nxt]
        path.append(v)          # close each lap
    return path


# Laps needed so that cost matches the final distances
laps_needed = {v: int((dist_frozen[v] - dist_final[v]) / -cycle_weight)
               if v in neg_cycle else 0
               for v in range(V)}


# ── 5. Console output ──────────────────────────────────────────────
print("=== Bellman–Ford ===")
print(f"Negative cycle path: {cycle}")
print(f"\nDistances (frozen) : {dist_frozen}")
print("Shortest Paths from Source — frozen distances:")
for v in range(V):
    laps = 1 if v in neg_cycle else 0
    path = path_with_laps(v, laps)
    note = f" (negative cycle taken {laps} time{'s'*(laps>1)})" if laps else ""
    print(f"Vertex {v}: Path = {path}, Total Cost = {dist_frozen[v]}{note}")
print(f"\nFinal Distances    : {dist_final}")
print("Shortest Paths from Source — final distances:")
for v in range(V):
    laps = laps_needed[v] + (1 if v in neg_cycle else 0)  # one extra on top
    path = path_with_laps(v, laps)
    note = f" (negative cycle taken {laps} time{'s'*(laps>1)})" if laps else ""
    print(f"Vertex {v}: Path = {path}, Total Cost = {dist_final[v]}{note}")

print("\n=== Dijkstra ===")
try:
    d_dist, _ = dijkstra(G, 0)
    print(f"Distances          : {d_dist}")
except ValueError as err:
    print(err)
