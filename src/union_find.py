

class UnionFind(object):
    "quick UnionFind implementation with path compression"
    def __init__(self, N):
        self.n_sets = N
        self.parents = range(N)
        self.ranks = [0] * N
        self._encode = {}
        self._decode = []

    def encode(self, x):
        if x not in self._encode:
            idx = len(self._decode)
            self._encode[x] = idx
            self._decode.append(x)
            return idx
        return self._encode[x]

    def decode(self, idx):
        return self._decode[idx]

    def _find(self, x):
        if x == self.parents[x]:
            return x
        else:
            root_x = self._find(self.parents[x])
            self.parents[x] = root_x
            return root_x

    def find(self, x):
        idx = self.encode(x)
        return self._find(idx)

    def _union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return
        if self.ranks[root_x] > self.ranks[root_y]:
            self.parents[root_y] = root_x
        elif self.ranks[root_x] < self.ranks[root_y]:
            self.parents[root_x] = root_y
        else:                   # not yet connected
            self.parents[root_y] = root_x
            self.ranks[root_x] += 1
        self.n_sets -= 1

    def union(self, *xs):
        for x, y in zip(xs[::2], xs[1::2]):
            self._union(x, y)

    def _connected(self, x, y):
        return self.find(x) == self.find(y)

    def connected(self, *xs):
        for x, y in zip(xs[::2], xs[1::2]):
            if not self._connected(x, y):
                return False
        return True


if __name__ == '__main__':
    edges = [
        ["0", "1"],
        ["1", "2"],
        ["2", "3"],
        ["5", "6"],
        ["7", "1"]
    ]
    uf = UnionFind(8)
    for x, y in edges:
        uf.union(x, y)
    assert uf.find("0") == uf.find("1")
    assert uf.find("0") == uf.find("2")
    assert uf.find("0") == uf.find("3")
    assert uf.find("0") != uf.find("4")
    assert uf.find("0") != uf.find("5")
    assert uf.find("4") != uf.find("5")
    assert uf.find("5") == uf.find("6")
    assert uf.find("7") == uf.find("0")
