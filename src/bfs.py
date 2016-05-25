# coding: utf-8

from collections import deque

INF = float("inf")


class BreadthFirstSearch(object):
    def __init__(self, graph, source):
        self._marked = set()
        self.edge_to = [None] * graph.V
        self.dist_to = [INF] * graph.V
        if hasattr(source, '__iter__'):
            self.hyperbfs(graph, source)
        else:
            self.bfs(graph, source)

    def _bfs_loop(self, graph, q):
        while len(q) != 0:
            v = q.popleft()
            for w in graph.adj(v):
                if w not in self._marked:
                    assert self.dist_to[v] != INF
                    self.edge_to[w] = v
                    self.dist_to[w] = self.dist_to[v] + 1
                    self._marked.add(w)
                    q.append(w)

    def bfs(self, graph, v):
        q = deque()
        self.dist_to[v] = 0
        self._marked.add(v)
        q.append(v)
        self._bfs_loop(graph, q)

    def hyperbfs(self, graph, vs):
        q = deque()
        for v in vs:
            self._marked.add(v)
            self.dist_to[v] = 0
            q.append(v)
        self._bfs_loop(graph, q)

    def has_path(self, v):
        return v in self._marked

    def path_to(self, v):
        if not self.has_path(v):
            return
        path = deque()
        x = v
        while self.dist_to[x] != 0:
            path.appendleft(x)
            x = self.edge_to[x]
        path.appendleft(x)
        return path
