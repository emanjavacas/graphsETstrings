
from src.graph import Graph
from src.digraph import DirectedCycle


class DirectedEdge(object):
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

    def origin(self):
        return self.v

    def target(self):
        return self.w

    def __str__(self):
        return "%d->%d (%.2f)" % (self.v, self.w, self.weight)


class WeightedDigraph(Graph):
    def __init__(self, V):
        super(WeightedDigraph, self).__init__(V)

    def add_edge(self, v, w, weight):
        self._validate_vertex(v), self._validate_vertex(w)
        self.E += 1
        edge = DirectedEdge(v, w, weight)
        self._adj[v].append(edge)


class WeightedDirectedCycle(DirectedCycle):
    def __init__(self, graph):
        super(WeightedDirectedCycle, self).__init__(graph)

    def dfs(self, graph, v):
        self._on_stack[v] = True
        self._marked.add(v)
        for e in graph.adj(v):
            w = e.target()
            if self.has_cycle():
                return
            if not self.marked(w):
                self._edge_to[w] = e
                self.dfs(graph, w)
            elif self._on_stack[w]:  # found cycle
                self._find_cycle(e, w)
        self._on_stack[v] = False

    def _find_cycle(self, e, w):
        cycle, x = [], e
        while x.origin() != w:
            cycle.append(x)
            x = self._edge_to[x.origin()]
        cycle.append(x)
        self.cycles.append(cycle)
