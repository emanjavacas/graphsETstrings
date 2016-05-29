
from Queue import PriorityQueue

from src.pqueue import pqueue
from src.weighted_graph import WeightedGraph
from src.union_find import UnionFind


class MST(object):
    def __init__(self, graph):
        if not isinstance(graph, WeightedGraph):
            raise ValueError("graph must be edge-weighted")
        self.graph = graph
        self.mst = []

    def edges(self):
        return self.mst

    def weight(self):
        return sum([e.weight for e in self.edges()])


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
        while len(self.edges()) != graph.V - 1 and not q.empty():
            e = q.get()
            v = e.either()
            w = e.other(v)
            if not uf.connected(v, w):  # not in a cycle
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
        self._marked = set()
        self._q = PriorityQueue()
        for v in graph.vertices():  # find minimum spanning forests
            if not self.marked(v):
                self.prim(graph, v)

    def prim(self, graph, source):
        self.visit(graph, source)
        while not self._q.empty():
            e = self._q.get()
            v = e.either()
            w = e.other(v)
            if self.marked(v) and self.marked(w):
                continue  # only disregard once we are prompted to consider
            self.mst.append(e)
            if not self.marked(v):
                self.visit(graph, v)
            if not self.marked(w):
                self.visit(graph, w)

    def visit(self, graph, v):
        self._marked.add(v)
        for e in graph.adj(v):
            if not self.marked(e.other(v)):
                self._q.put(e)

    def marked(self, v):
        return v in self._marked


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
        self._edge_to = [None] * graph.V
        self._dist_to = [float("inf")] * graph.V
        self._marked = set()
        self._q = pqueue()
        for v in graph.vertices():
            if not self.marked(v):
                self.prim(graph, v)

    def prim(self, graph, source):
        self._dist_to[source] = 0.0
        self._q.enqueue((self._dist_to[source], source))
        while not self._q.empty():
            v = self._q.dequeue()
            self.visit(graph, v)

    def visit(self, graph, v):
        self._marked.add(v)
        for e in graph.adj(v):
            w = e.other(v)
            if self.marked(w):
                continue
            if e.weight < self._dist_to[w]:  # always maintain only the closest
                self._dist_to[w] = e.weight
                self._edge_to[w] = e
                self._q.update(e.weight, w)

    def edges(self):
        return [e for e in self._edge_to if e is not None]

    def marked(self, v):
        return v in self._marked


if __name__ == '__main__':
    from argparse import ArgumentParser
    import sys

    parser = ArgumentParser(description='graph main')
    parser.add_argument('-a', '--algorithm', default='kruskal')
    parser.add_argument('-f', '--fname')
    parser.add_argument('-s', '--source', type=int)
    parser.add_argument('-S', '--sep')

    args = vars(parser.parse_args())

    graph = WeightedGraph.from_file(args['fname'])

    if args['algorithm'] == 'kruskal':
        mst = KruskalMST(graph)
    elif args['algorithm'] == 'lazyPrim':
        mst = LazyPrimMST(graph)
    elif args['algorithm'] == 'eagerPrim':
        mst = EagerPrimtMST(graph)
    elif args['algorithm'] == 'all':
        kruskal = sorted(KruskalMST(graph).edges())
        lazy = sorted(LazyPrimMST(graph).edges())
        eager = sorted(EagerPrimtMST(graph).edges())
        print("kruskal == lazy [%s]" % str(kruskal == lazy))
        print("kruskal == eager [%s]" % str(kruskal == eager))
        print("eager == lazy [%s]" % str(eager == lazy))
        sys.exit(0)
    else:
        print("No matching algorithm (kruskal,lazyPrim,eagerPrim)")
        sys.exit(1)

    for edge in mst.edges():
        print(edge)
    print("%.5f" % mst.weight())
    print(str(len(mst.edges())))
