from src.union_find import UnionFind

edges = [
    ["0", "1"],
    ["1", "2"],
    ["2", "3"],
    ["5", "6"],
    ["7", "1"]
]


def union_find():
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
