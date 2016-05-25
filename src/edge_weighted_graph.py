# coding: utf-8

from src.graph import Graph


class Edge(object):
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

    def either(self):
        "allows for v = e.either(), w = e.either(v)"
        return self.w

    def other(self, v):
        if v == self.v:
            return self.w
        elif v == self.w:
            return self.v
        raise ValueError("Argument doesn't correspond to either edge vertex")

    def __cmp__(self, other):
        return cmp(self.weight, other.weight)

    def __str__(self):
        pass


class EdgeWeightedGraph(Graph):
    def __init__(self, V):
        super(EdgeWeightedGraph, self).__init__(V)

    def add_edge(self, v, w, weight):
        self._validate_vertex(v), self._validate_vertex(w)
        self.E += 1
        edge = Edge(v, w, weight)
        self._adj[v].append(edge)
        self._adj[w].append(edge)

    def edges(self):
        edges = []
        for v in range(self.V):
            self_loops = 0
            for e in self.adj(v):
                if e.other(v) > v:
                    edges.append(e)
                elif e.other(v) == v:
                    if self_loops % 2 == 0:  # self loops will be consecutive
                        edges.append(e)
                    self_loops += 1
        return edges
