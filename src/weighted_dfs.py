
from src.weighted_digraph import WeightedDirectedCycle
from src.dfs import DepthFirstOrder, TopologicalSort


class WeightedDepthFirstOrder(DepthFirstOrder):
    def __init__(self, graph):
        super(WeightedDepthFirstOrder, self).__init__(graph)

    def dfs(self, graph, v):
        self._marked.add(v)
        self.pre[v] = len(self.preorder)
        self.preorder.append(v)
        for e in graph.adj(v):
            w = e.target()
            if not self.marked(w):
                self.dfs(graph, w)
        self.post[v] = len(self.postorder)
        self.postorder.append(v)


class WeightedTopologicalSort(TopologicalSort):
    def __init__(self, graph):
        self.order = None
        cycle = WeightedDirectedCycle(graph)
        if not cycle.has_cycle():
            searcher = WeightedDepthFirstOrder(graph)
            self.order = searcher.reverse_post()
