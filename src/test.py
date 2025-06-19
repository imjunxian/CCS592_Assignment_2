"""
Builds the assignment graph, runs Bellman–Ford and Dijkstra, and prints
results.  Demonstrates that Dijkstra rejects negative edges.
"""

from graph import DiGraph
from bellman_ford import bellman_ford
from dijkstra import dijkstra

# -------- assignment graph (directed, weighted) -------------------------
V = 6
E = [
    (0, 2,  5),
    (0, 1,  4),
    (2, 1, -2),
    (1, 3,  3),
    (3, 4,  2),
    (4, 5, -1),
    (5, 3, -2),
]

g = DiGraph.from_edges(V, E)

print("=== Bellman–Ford ===")
dist, parent, neg = bellman_ford(V, g.edges(), src=0)
print("Distances :", dist)
print("Neg-cycle :", neg)

print("\n=== Dijkstra ===")
try:
    d_dist, d_parent = dijkstra(g, src=0)
    print("Distances :", d_dist)
except ValueError as err:
    print(err)
