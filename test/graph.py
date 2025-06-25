"""
Lightweight directed, weighted graph.

Vertices are labelled 0..V-1.
Edges are stored as 3-tuples (u, v, w).

Only a tiny feature addition: an `edges_list()` helper that
materialises the edge generator so other algorithms can iterate
over it multiple times.
"""
from collections import defaultdict
from typing import Dict, Iterable, Iterator, List, Tuple

Edge = Tuple[int, int, int]        # (u, v, weight)


class DiGraph:
    def __init__(self, num_vertices: int) -> None:
        self.V: int = num_vertices
        self._adj: Dict[int, List[Tuple[int, int]]] = defaultdict(list)

    # ── mutators ────────────────────────────────────────────────
    def add_edge(self, u: int, v: int, w: int) -> None:
        if not (0 <= u < self.V and 0 <= v < self.V):
            raise ValueError("vertex id out of range")
        self._adj[u].append((v, w))

    def add_edges(self, edges: Iterable[Edge]) -> None:
        for u, v, w in edges:
            self.add_edge(u, v, w)

    # ── accessors ───────────────────────────────────────────────
    def neighbours(self, u: int) -> List[Tuple[int, int]]:
        return self._adj[u]

    def edges(self) -> Iterator[Edge]:
        for u, nbrs in self._adj.items():
            for v, w in nbrs:
                yield (u, v, w)

    def edges_list(self) -> List[Edge]:
        """Return all edges in a list (useful for multiple passes)."""
        return list(self.edges())

    # ── convenience ─────────────────────────────────────────────
    @classmethod
    def from_edges(cls, num_vertices: int, edges: Iterable[Edge]):
        g = cls(num_vertices)
        g.add_edges(edges)
        return g

    def __str__(self) -> str:
        return "\n".join(f"{u} → {v} ({w})" for u, v, w in self.edges())
