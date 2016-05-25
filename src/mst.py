
from Queue import PriorityQueue

from pqueue import pqueue

from src.union_find import UnionFind
from src.edge_weighted_graph import edgeWeightedGraph


class MST(object):
    def __init__(self, graph):
        if not isinstance(graph, edgeWeightedGraph):
            raise ValueError("graph must be edge-weighted")
        self.graph = graph
        self.mst = []

    def edges(self):
        return self.mst


class KruskalMST(MST):
    def __init__(self, graph):
        """
        Grow the tree by adding the minimum-weight edge not entailing a cycle.
        """
        super(KruskalMST, self).__init__(graph)
        q = PriorityQueue()
        for e in graph.edges():
            q.put(e)
        uf = UnionFind(graph.V)
        while len(self.mst.edges()) != graph.V - 1 and not q.empty():
            e = q.get()
            v = e.either()
            w = e.other(v)
            if not uf.connected(v, w):  # not in a loop
                uf.union(v, w)
                self.mst.append(e)


class LazyPrimMST(MST):
    def __init__(self, graph):
        """
        Grow the tree by adding the minimum-weight crossing edge. Lazy version
        finds the minimum-weight crossing edge as the min element in a
        PriorityQueue of edges adjacent to vertices in the tree but not yet
        in the tree (at most one of the vertices in the edge has been visited)
        """
        super(LazyPrimMST, self).__init__(graph)
        self.weight = 0
        self._marked = set()
        self._q = PriorityQueue()
        for v in graph.vertices():  # also works for not connected graphs?
            if not self.marked(v):
                self.prim(graph, v)

    def prim(self, graph, source):
        self.visit(graph, source)
        while not self._q.empty():
            e = self._q.get()
            v = e.either()
            w = e.other(v)
            if self.marked(v, w):
                continue
            self.mst.append(e)
            if not self.marked(v):
                self.visit(graph, v)
            if not self._marked(w):
                self.visit(graph, w)

    def visit(self, graph, v):
        self._marked.add(v)
        for e in graph.adj(v):
            if not self.marked(e.other(v)):
                self._q.put(e)

    def marked(self, v, *vs):
        self._marked.add(v)
        for v in vs:
            self._marked(v)


class EagerPrimtMST(MST):
    def __init__(self, graph):
        """
        Grow the tree by adding the minimum-weight crossing edge. Eager version
        finds the minimum-weight crossing edge as the min element in a
        PriorityQueue of vertices that are connected to vertices in the tree
        with (updated) priority equal to the min edge adjacent to the vertex.
        Note that only one edge per vertex adjacent to the tree is considered.
        """
        super(EagerPrimtMST, self).__init__(graph)
        self._q = pqueue()
        self._marked = set()
        self._dist_to = [float("inf")] * graph.V
        self._edge_to = [None] * graph.V
        for v in graph.vertices():
            if not self.marked(v):
                self.prim(graph, v)

        def prim(self, graph, source):
            self._dist_to[source] = 0.0
            self._q.enqueue((self.dist_to[source], source))
            while not self._q.empty():
                v = self._q.dequeue()
                self.visit(graph, v)

        def visit(self, graph, v):
            self._marked.add(v)
            for e in graph.adj(v):
                w = e.other(v)
                if not self.marked(w) and w.weight < self._dist_to[w]:
                    self._dist_to[w] = w.weight
                    self._edge_to[w] = e
                    self._q.update((e.weight, w))
                self.mst.append(v)

        def edges(self):
            return [e for e in self._edge_to if e is not None]

        def marked(self, v):
            return v in self._marked
