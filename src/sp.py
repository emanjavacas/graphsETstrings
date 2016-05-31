
from src.pqueue import pqueue
from src.weighted_dfs import WeightedTopologicalSort
from src.weighted_digraph import WeightedDigraph, WeightedDirectedCycle


class SP(object):
    def __init__(self, graph, source):
        """SP represents the shortest directed path tree with two lists.
        Shortest paths s->...->(v1,2,...,vk) are computed iff:
        -> _dist_to[v] is the length of some path from s to v
        -> for each edge (v->w), _dist_to[w] <= _dist_to[v] + e.weight
        (the equal may refer to the case where s->w goes through v)"""
        self._dist_to = [float("inf")] * graph.V
        self._edge_to = [None] * graph.V
        self._dist_to[source] = 0.0

    def dist_to(self, v):
        return self._dist_to[v]

    def has_path_to(self, v):
        return self._dist_to[v] < float("inf")

    def path_to(self, v):
        path = []
        e = self._edge_to[v]
        if e is None:
            return []
        path = [e] + path
        while e is not None:
            e = self._edge_to[e.origin()]
            path = [e] + path
        return path

    def relax(self, e):
        v, w = e.origin(), e.target()
        if self.dist_to(w) > self.dist_to(v) + e.weight:
            self._dist_to[w] = self.dist_to(v) + e.weight
            self._edge_to[w] = e


class DijkstraSP(SP):
    def __init__(self, graph, source):
        super(DijkstraSP, self).__init__(graph, source)
        self._q = pqueue()
        self._q.enqueue((0.0, source))
        while len(self._q) != 0:
            v = self._q.dequeue()
            for e in graph.adj(v):
                self.relax(e)

    def relax(self, e):
        v, w = e.origin(), e.target()
        if self.dist_to(w) > self.dist_to(v) + e.weight:
            self._dist_to[w] = self.dist_to(v) + e.weight
            self._edge_to[w] = e
            self._q.update(self.dist_to(w), w)


class AcyclicSP(SP):
    def __init__(self, graph, source):
        super(AcyclicSP, self).__init__(graph, source)
        topological = WeightedTopologicalSort(graph)
        if not topological.has_order():
            raise ValueError("Weighted Digraph has cycles")
        for v in topological.order:
            for e in graph.adj(v):
                self.relax(e)


class BellmanFord(SP):
    def __init__(self, graph, source):
        super(BellmanFord, self).__init__(graph, source)
        self._on_queue = [False] * graph.V
        self._q = []
        self._q = [source] + self._q
        self._on_queue[source] = True
        self._cost = 0
        self._cycle = []
        while len(self._q) != 0 and not self.has_negative_cycle():
            v = self._q.pop()
            self._on_queue[v] = False
            self.relax(graph, v)

    def has_negative_cycle(self):
        return bool(self._cycle)

    def negative_cycle(self):
        return self._cycle

    def relax(self, graph, v):
        for e in graph.adj(v):
            w = e.target()
            if self.dist_to(w) > self.dist_to(v) + e.weight:
                self._dist_to[w] = self.dist_to(v) + e.weight
                self._edge_to[w] = e
                if not self._on_queue[w]:
                    self._on_queue[w] = True
                    self._q = [w] + self._q
            self._find_negative_cycle(graph)
            if self.has_negative_cycle():
                return

    def _find_negative_cycle(self, graph):
        self._cost += 1
        if self._cost % graph.V == 0:
            wdg = WeightedDigraph(graph.V)
            for v in graph.vertices():
                if self._edge_to[v]:
                    e = self._edge_to[v]
                    v, w, weight = e.origin(), e.target(), e.weight
                    wdg.add_edge(v, w, weight)
            cycle = WeightedDirectedCycle(wdg)
            self._cycle = cycle.cycle()

if __name__ == '__main__':
    from argparse import ArgumentParser
    import sys

    parser = ArgumentParser(description='Shortest paths')
    parser.add_argument('action', default='dijkstra')
    parser.add_argument('-f', '--fname')
    parser.add_argument('-s', '--source', type=int)

    args = vars(parser.parse_args())

    fname = args['fname']
    source = args['source']
    graph = WeightedDigraph.from_file(fname)

    if args['action'] == 'dijkstra':
        sp = DijkstraSP(graph, source)
    elif args['action'] == 'acyclic':
        sp = AcyclicSP(graph, source)
    elif args['action'] == 'bellman':
        sp = BellmanFord(graph, source)
        if sp.has_negative_cycle():
            for e in sp.negative_cycle():
                print(e)
            sys.exit(1)

    for v in graph.vertices():
        dist = "%d to %d (%.2f): " % (source, v, sp.dist_to(v))
        path = "\t".join([str(e) if e else "" for e in sp.path_to(v)])
        print(dist + path)
