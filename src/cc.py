# coding: utf-8


class ConnectedComponents(object):
    def __init__(self, graph):
        self._marked = set()
        self.ids = [None] * graph.V
        self.size = [0] * graph.V
        self._count = 0
        for v in range(graph.V):
            if v not in self._marked:
                self.dfs(graph, v)
                self._count += 1

    def dfs(self, graph, v):
        self._marked.add(v)
        self.ids[v] = self._count
        self.size[self._count] += 1
        for w in graph.adj(v):
            if w not in self._marked:
                self.dfs(graph, w)

    def connected(self, v, w):
        return self.ids[v] == self.ids[w]

    def components(self):
        cs = [[] for c in range(self._count)]
        for v in range(len(self._marked)):
            cs[self.ids[v]].append(v)
        return cs

    def marked(self, v):
        return v in self._marked

    def count(self):
        return self._count
