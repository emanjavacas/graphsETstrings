# coding: utf-8

from bfs import BreadthFirstSearch
from dfs import DepthFirstPaths, DepthFirstSearch
from cc import ConnectedComponents

from argparse import ArgumentParser


class Graph(object):
    def __init__(self, V):
        self.V = V
        self.E = 0
        self._adj = [list() for i in range(V)]

    def _validate_vertex(self, v):
        assert v >= 0 and v < self.V

    def add_edge(self, v, w, **kwargs):
        self._validate_vertex(v), self._validate_vertex(w)
        self.E += 1
        self._adj[w].append(v)
        self._adj[v].append(w)

    def adj(self, v):
        self._validate_vertex(v)
        return self._adj[v]

    def degree(self, v):
        self._validate_vertex(v)
        return len(self._adj[v])

    @classmethod
    def from_file(cls, fname):
        with open(fname, 'r') as f:
            V = int(next(f))
            graph = cls(V)
            next(f)
            for line in f:
                line = line.strip().split()
                v, w, weight = line[0], line[1], line[2:]
                weight = int(weight) if weight else 0
                graph.add_edge(int(v), int(w), weight=weight)
        return graph

    def __str__(self):
        s = str(self.V) + " vertices, " + str(self.E) + " edges"
        s += "\n"
        for i, bag in enumerate(self._adj):
            s += str(i) + ": " + " ".join([str(v) for v in bag]) + "\n"
        return s


class SymbolGraph(object):
    def __init__(self, lines, sep=' '):
        self._st = {}
        lines = list(lines)
        for line in lines:
            for v in line.strip().split(sep):
                if v not in self._st:
                    self._st[v] = len(self._st)
        self._keys = \
            [k for (k, v) in sorted(self._st.items(), key=lambda x: x[1])]
        self.graph = Graph(len(self._st))
        for line in lines:
            l = line.strip().split(sep)
            v, ws = l[0], l[1:]
            for w in ws:
                self.graph.add_edge(self._st[v], self._st[w])

    @staticmethod
    def from_file(fname, sep=' '):
        with open(fname, 'r') as f:
            lines = [l for l in f]
        return SymbolGraph(lines, sep=sep)

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
    parser.add_argument('-S', '--sep')

    args = vars(parser.parse_args())

    fname = args['fname']
    action = args['action']

    # Print graph
    if action == 'graph':
        graph = Graph.from_file(fname)
        print graph

    # Connected?
    elif action == 'connected':
        source = args['source']
        graph = Graph.from_file(fname)
        searcher = DepthFirstSearch(graph, source)
        print(" ".join([str(v) for v in range(graph.V) if searcher.marked(v)]))
        print("Connected" if searcher.connected() else "NOT Connected")

    # Path to vertex with DFS
    elif action == 'DFSpath':
        source = args['source']
        graph = Graph.from_file(fname)
        paths = DepthFirstPaths(graph, source)
        for v in range(graph.V):
            if paths.has_path(v):
                print("%d to %d: " % (source, v) +
                      " -> ".join([str(i) for i in paths.path_to(v)]))
            else:
                print("%d to %d: not connected" % (source, v))

    # Shortest paths with BFS
    elif action == 'BFSpath':
        source = args['source']
        graph = Graph.from_file(fname)
        paths = BreadthFirstSearch(graph, source)
        for v in range(graph.V):
            if paths.has_path(v):
                print("%d to %d: " % (source, v) +
                      " -> ".join([str(i) for i in paths.path_to(v)]))
            else:
                print("%d to %d: not connected" % (source, v))

    # Connected components
    elif action == 'CC':
        graph = Graph.from_file(fname)
        cc = ConnectedComponents(graph)
        print("%d components" % cc.count())
        for c, nodes in enumerate(cc.components()):
            print("%d: %s" % (c, " ".join([str(v) for v in nodes])))

    # SymbolGraph
    elif action == 'symbolGraph':
        sep = args['sep']
        with open(fname, 'r') as f:
            lines = [l for l in f]
        sgraph = SymbolGraph(lines, sep=sep)
        while True:
            source = raw_input("insert a connection or exit:\n")
            if source == 'exit':
                print("Bye!")
                break
            for w in sgraph.graph.adj(sgraph.int(source)):
                print("   " + sgraph.name(w))
