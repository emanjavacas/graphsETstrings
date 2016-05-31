#!/usr/bin/env python

from argparse import ArgumentParser

from graph import Graph
from dfs import DirectedDFS, DepthFirstOrder
from dfs import TopologicalSort, KosarajuSharirSCC
from bfs import BreadthFirstSearch


class Digraph(Graph):
    def __init__(self, V):
        super(Digraph, self).__init__(V)

    def add_edge(self, v, w, **kwargs):
        self._validate_vertex(v), self._validate_vertex(w)
        self.E += 1
        self._adj[v].append(w)

    def reverse(self):
        graph = Digraph(self.V)
        for v in self.vertices():
            for w in self.adj(v):
                graph.add_edge(w, v)
        return graph


class DirectedCycle(object):
    def __init__(self, graph):
        self._marked = set()
        self._edge_to = [None] * graph.V
        self._on_stack = [False] * graph.V
        self.cycles = []
        for v in graph.vertices():
            if not self.marked(v):
                self.dfs(graph, v)

    def marked(self, v):
        return v in self._marked

    def dfs(self, graph, v):
        self._on_stack[v] = True
        self._marked.add(v)
        for w in graph.adj(v):
            if self.has_cycle():
                return
            if not self.marked(w):
                self._edge_to[w] = v
                self.dfs(graph, w)
            elif self._on_stack[w]:  # found cycle
                self._find_cycle(v, w)
        self._on_stack[v] = False

    def _find_cycle(self, v, w):
        cycle, x = [], v
        while x != w:
            cycle.append(x)
            x = self._edge_to[x]
        cycle.append(w), cycle.append(v)
        self.cycles.append(cycle)

    def has_cycle(self):
        return bool(self.cycles)

    def cycle(self):
        "returns last cycle"
        if not self.has_cycle():
            return []
        return self.cycles[-1]


class SymbolDigraph(object):
    def __init__(self, lines, sep=' '):
        self._st = {}
        lines = list(lines)
        for line in lines:
            for v in line.strip().split(sep):
                if v not in self._st:
                    self._st[v] = len(self._st)
        self._keys = \
            [k for (k, v) in sorted(self._st.items(), key=lambda x: x[1])]
        self.graph = Digraph(len(self._st))
        for line in lines:
            l = line.strip().split(sep)
            v, ws = l[0], l[1:]
            for w in ws:
                self.graph.add_edge(self._st[v], self._st[w])

    @staticmethod
    def from_file(fname, sep=' '):
        with open(fname, 'r') as f:
            lines = [l for l in f]
        return SymbolDigraph(lines, sep=sep)

    def contains(self, s):
        return s in self._st

    def int(self, s):
        return self._st[s]

    def name(self, v):
        return self._keys[v]


if __name__ == '__main__':
    parser = ArgumentParser(description='graph main')
    parser.add_argument('action', default='graph')
    parser.add_argument('-f', '--fname')
    parser.add_argument('-s', '--source', type=int)
    parser.add_argument('-S', '--sources', type=int, nargs='+')
    parser.add_argument('-d', '--delim', type=str)

    args = vars(parser.parse_args())

    fname = args['fname']
    action = args['action']

    if action == 'directedDFS':
        graph = Digraph.from_file(fname)
        searcher = DirectedDFS.from_sources(graph, map(int, args['sources']))
        print(" ".join([str(v) for v in graph.vertices() if searcher.marked(v)]))

    if action == 'cycle':
        graph = Digraph.from_file(fname)
        cycle = DirectedCycle(graph)
        if cycle.has_cycle():
            print("%d cycles found" % len(cycle.cycles))
            for c in cycle.cycles:
                print("Cycle: " + " -> ".join([str(v) for v in c]))
        else:
            print("No Cycles found")

    elif action == 'dfs-order':
        graph = Digraph.from_file(fname)
        dfs_order = DepthFirstOrder(graph)
        print("   v  pre post")
        print("--------------")
        for v in graph.vertices():
            print("%4d %4d %4d" % (v, dfs_order.pre[v], dfs_order.post[v]))
        print("Preorder:")
        print(" ".join([str(v) for v in dfs_order.preorder]))
        print("Postorder:")
        print(" ".join([str(v) for v in dfs_order.postorder]))
        print("Reverse postorder:")
        print(" ".join([str(v) for v in dfs_order.reverse_post()]))

    elif action == 'topological':
        delim = args['delim']
        sg = SymbolDigraph.from_file(fname, sep=delim)
        topological = TopologicalSort(sg.graph)
        for v in topological.order:
            print(sg.name(v))

    elif action == 'strongly_connected':
        delim = args['delim']
        sg = SymbolDigraph.from_file(fname, sep=delim)
        scc = KosarajuSharirSCC(sg.graph)
        for v in sorted([sg.name(x) for x in sg.graph.vertices()]):
            print("%s: %d" % (v, scc.ids[sg.int(v)]))

    elif action == 'BFSpath':
        source = args['source']
        graph = Digraph.from_file(fname)
        paths = BreadthFirstSearch(graph, source)
        for v in graph.vertices():
            if paths.has_path(v):
                print("%d to %d: " % (source, v) +
                      " -> ".join([str(i) for i in paths.path_to(v)]))
            else:
                print("%d to %d: not connected" % (source, v))

    if action == 'graph':
        graph = Digraph.from_file(fname)
        print(graph)
