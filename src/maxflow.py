
from src.graph import Graph


class FlowEdge(object):
    def __init__(self, v, w, capacity):
        self.v = v
        self.w = w
        self.capacity = capacity
        self.flow = 0.0

    def origin(self):
        return self.v

    def target(self):
        return self.w

    def other(self, v):
        if v == self.v:
            return self.w
        elif v == self.w:
            return self.v

    def residual(self, v):
        if v == self.v:         # backward edge
            return self.flow
        elif v == self.w:       # forward edge
            return self.capacity - self.flow
        else:
            raise ValueError("non-existing vertex [%d]" % v)

    def add_residual(self, v, delta):
        if v == self.v:         # backward edge
            self.flow -= delta
        elif v == self.w:       # forward edge
            self.flow += delta
        else:
            raise ValueError("non-existing vertex [%d]" % v)


class FlowNetwork(Graph):
    def __init__(self, V):
        super(FlowNetwork, self).__init__(V)

    def add_edge(self, v, w, capacity):
        edge = FlowEdge(v, w, capacity)
        self._adj[v].append(edge)
        self._adj[w].append(edge)


class FordFulkerson(object):
    def __init__(self, graph, s, t):
        self._marked = set(),
        self._edge_to = []  # last edge on s->v path (see has_augmenting_path)
        self._value = 0.0

        while self.has_augmenting_path(graph, s, t):
            bottle = float("inf")
            v = t
            while v != s:
                bottle = min(bottle, self._edge_to[v].residual(v))
                v = self._edge_to[v].other(v)
            v = t
            while v != s:
                self._edge_to[v].add_residual(v, bottle)
                v = self._edge_to[v].other(v)
            self._value += bottle

    def has_augmenting_path(self, graph, s, t):
        self._edge_to, self._marked, q = [], [], [s]
        self._marked.add(s)
        while len(q) != 0:
            v = q.pop()
            for e in graph.adj(v):
                w = v.other()
                if e.residual(w) > 0 and not self.marked(w):
                    self._edge_to[w] = e
                    self._marked.add(w)
                    q = [w] + q
        return self.marked(t)

    def marked(self, v):
        return v in self._marked
