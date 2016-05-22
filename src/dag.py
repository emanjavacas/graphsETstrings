#!/usr/bin/env python
from argparse import ArgumentParser
from collections import deque

from dfs import DirectedDFS, DepthFirstOrder
from dfs import TopologicalSort, KosarajuSharirSCC


class Digraph(object):
    def __init__(self, V):
        self.V = V
        self.E = 0
        self._adj = [deque() for i in range(V)]

    def _validate_vertex(self, v):
        assert v >= 0 and v < self.V

    def add_edge(self, v, w):
        self._validate_vertex(v)
        self._validate_vertex(w)
        self.E += 1
        self._adj[v].appendleft(w)

    def adj(self, v):
        self._validate_vertex(v)
        return self._adj[v]

    def degree(self, v):
        self._validate_vertex(v)
        return len(self._adj[v])

    def reverse(self):
        graph = Digraph(self.V)
        for v in range(self.V):
            for w in self.adj(v):
                graph.add_edge(w, v)
        return graph

    @staticmethod
    def from_file(fname):
        with open(fname, 'r') as f:
            V = int(next(f))
            graph = Digraph(V)
            next(f)
            for line in f:
                v, w = line.strip().split()
                graph.add_edge(int(v), int(w))
        return graph

    def __str__(self):
        s = str(self.V) + " vertices, " + str(self.E) + " edges"
        s += "\n"
        for i, bag in enumerate(self._adj):
            s += str(i) + ": " + " ".join([str(v) for v in bag]) + "\n"
        return s


class DirectedCycle(object):
    def __init__(self, digraph):
        self._marked = [False] * digraph.V
        self.edge_to = [None] * digraph.V
        self.on_stack = [False] * digraph.V
        self.cycles = []
        for v in range(digraph.V):
            if not self._marked[v]:
                self.dfs(digraph, v)

    def dfs(self, digraph, v):
        self.on_stack[v] = True
        self._marked[v] = True
        for w in digraph.adj(v):
            if self.has_cycle():
                return
            if not self._marked[w]:
                self.edge_to[w] = v
                self.dfs(digraph, w)
            elif self.on_stack[w]:  # found cycle
                cycle = []
                x = v
                while x != w:
                    cycle.append(x)
                    x = self.edge_to[x]
                cycle.append(w)
                cycle.append(v)
                self.cycles.append(cycle)
            self.on_stack[v] = False

    def has_cycle(self):
        return bool(self.cycles)


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
        print(" ".join([str(v) for v in range(graph.V) if searcher.marked(v)]))

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
        for v in range(graph.V):
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
        digraph = sg.graph
        scc = KosarajuSharirSCC(digraph)
        for v in sorted([sg.name(x) for x in range(digraph.V)]):
            print("%s: %d" % (v, scc.ids[sg.int(v)]))
