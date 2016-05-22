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

    def __str__(self):
        pass


class EdgeWeightedGraph(Graph):
    def __init__(self, V):
        super(EdgeWeightedGraph, self).__init__(V)

    def add_edge(self, v, w, weight):
        self._validate_vertex(v), self._validate_vertex(w)
        edge = Edge(v, w, weight)
        self._adj[v].append(edge)
        self._adj[w].append(edge)