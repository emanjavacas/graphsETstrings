# coding: utf-8
from collections import deque


class DepthFirstSearch(object):
    def __init__(self, graph, source):
        self._marked = [False] * graph.V
        self._count = 0
        self.dfs(graph, source)

    def dfs(self, graph, source):
        self._count += 1
        self._marked[source] = True
        for v in graph.adj(source):
            if not self._marked[v]:
                self.dfs(graph, v)

    def connected(self):
        return self._count == len(self._marked)  # graph.V

    def marked(self, v):
        return self._marked[v]

    def count(self, v):
        return self._count


class DepthFirstPaths(object):
    def __init__(self, graph, source):
        self._marked = [False] * graph.V
        self.edge_to = [None] * graph.V
        self.source = source
        self.dfs(graph, source)

    def dfs(self, graph, v):
        self._marked[v] = True
        for w in graph.adj(v):
            if not self._marked[w]:
                self.edge_to[w] = v
                self.dfs(graph, w)

    def has_path(self, v):
        return self._marked[v]

    def path_to(self, v):
        if not self.has_path(v):
            return
        path = deque()
        x = v
        while x != self.source:
            path.appendleft(x)   # first iter adds destination vertex
            x = self.edge_to[x]
        path.appendleft(x)              # adds origin vertex (self.source)
        return path

    def marked(self, v):
        return self._marked[v]

    def count(self, v):
        return self._count


class Cycle(object):
    def __init__(self, graph):
        self._marked = [False] * graph.V
        self._has_cycle = False
        for v in range(graph.V):
            if not self._marked[v]:
                self.dfs(graph, v, v)

    def dfs(self, graph, v, u):
        self._marked[v] = True
        for w in graph.adj(v):
            if not self._marked[w]:
                self.dfs(graph, w, v)
            elif w == u:
                self._has_cycle = True

    def has_cycle(self):
        return self._has_cycle


class DirectedDFS(object):
    def __init__(self, graph, source):
        self._marked = [False] * graph.V
        self.dfs(graph, source)

    def dfs(self, graph, v):
        self._marked[v] = True
        for w in graph.adj(v):
            if not self._marked[w]:
                self.dfs(graph, w)

    @classmethod
    def from_sources(cls, graph, sources):
        dfs = cls(graph, sources[0])
        for s in sources[1:]:
            dfs.dfs(graph, s)
        return dfs

    def marked(self, v):
        return self._marked[v]


class DepthFirstOrder(object):
    def __init__(self, graph):
        self._marked = [False] * graph.V
        self.pre = [None] * graph.V
        self.post = [None] * graph.V
        self.preorder = []
        self.postorder = []
        for v in range(graph.V):
            if not self._marked[v]:
                self.dfs(graph, v)

    def dfs(self, graph, v):
        self._marked[v] = True
        self.pre[v] = len(self.preorder)
        self.preorder.append(v)
        for w in graph.adj(v):
            if not self._marked[w]:
                self.dfs(graph, w)
        self.post[v] = len(self.postorder)
        self.postorder.append(v)

    def reverse_post(self):
        return self.postorder[::-1]

    def _check(self, graph):
        assert self.preorder == [self.pre[i] for i in range(graph.V)]
        assert self.postorder == [self.post[i] for i in range(graph.V)]


class TopologicalSort(object):
    def __init__(self, graph):
        self.order = None
        cycle = Cycle(graph)
        if not cycle.has_cycle():
            searcher = DepthFirstOrder(graph)
            self.order = searcher.reverse_post()
            self._rank = [i for i, v in sorted(enumerate(self.order),
                                               key=lambda x: x[1])]

    def has_order(self):
        return not self.order

    def rank(self, v):
        if self.has_order():
            return self._rank[v]


class KosarajuSharirSCC(object):
    def __init__(self, graph):
        self._marked = [False] * graph.V
        self.count = 0
        self.ids = [None] * graph.V
        reverse_post = DepthFirstOrder(graph.reverse()).reverse_post()
        for v in reverse_post:
            if not self._marked[v]:
                self.dfs(graph, v)
                self.count += 1

    def dfs(self, graph, v):
        self._marked[v] = True
        self.ids[v] = self.count
        for w in graph.adj(v):
            if not self._marked[w]:
                self.dfs(graph, w)

    def strongly_connected(self, v, w):
        return self.ids[v] == self.ids[w]
