# coding: utf-8

from collections import deque

INF = float("inf")


class BreadthFirstSearch(object):
    def __init__(self, graph, source):
        self.marked = [False] * graph.V
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
                if not self.marked[w]:
                    assert self.dist_to[v] != INF
                    self.edge_to[w] = v
                    self.dist_to[w] = self.dist_to[v] + 1
                    self.marked[w] = True
                    q.append(w)

    def bfs(self, graph, v):
        q = deque()
        self.dist_to[v] = 0
        self.marked[v] = True
        q.append(v)
        self._bfs_loop(graph, q)

    def hyperbfs(self, graph, vs):
        q = deque()
        for v in vs:
            self.marked[v] = True
            self.dist_to[v] = 0
            q.append(v)
        self._bfs_loop(graph, q)

    def has_path(self, v):
        return self.marked[v]

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
