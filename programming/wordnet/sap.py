
import argparse
import signal
import sys

from src.bfs import BreadthFirstSearch
from src.dag import Digraph


class SAP(object):
    def __init__(self, graph):
        self.graph = graph

    def _ancestor(self, v, w, bfs_v, bfs_w):
        ancestors = []
        for x in range(self.graph.V):  # TODO: iterate over v ancestors
            if bfs_v.has_path(x) and bfs_w.has_path(x):
                ancestors.append(x)
        if ancestors:
            return min(ancestors,
                       key=lambda x: bfs_v.dist_to[x] + bfs_w.dist_to[x])
        else:
            return -1

    def length(self, v, w):
        bfs_v = BreadthFirstSearch(self.graph, v)
        bfs_w = BreadthFirstSearch(self.graph, w)
        ancestor = self._ancestor(v, w, bfs_v, bfs_w)
        if ancestor == -1:
            return -1
        return bfs_v.dist_to[ancestor] + bfs_w.dist_to[ancestor]

    def ancestor(self, v, w):
        bfs_v = BreadthFirstSearch(self.graph, v)
        bfs_w = BreadthFirstSearch(self.graph, w)
        return self._ancestor(v, w, bfs_v, bfs_w)

    def hyperlength(self, vs, ws):
        pass

    def hyperancestor(self, vs, ws):
        pass


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda s, frame: sys.exit(0))

    usage = 'python -m programming.wordnet.sap -f data/digraph1.txt'
    parser = argparse.ArgumentParser(description='SAP', usage=usage)
    parser.add_argument('-f', '--fname')
    args = vars(parser.parse_args())

    graph = Digraph.from_file(args['fname'])
    sap = SAP(graph)

    def process_input(prompt):
        try:
            return int(prompt)
        except ValueError:
            return [int(i) for i in prompt.split(" ")]

    while True:
        v = process_input(raw_input("Insert a vertex or vertices\n"))
        w = process_input(raw_input("Insert a vertex or vertices\n"))
        length = sap.length(v, w)
        ancestor = sap.ancestor(v, w)
        print("length = %d, ancestor = %d" % (length, ancestor))
