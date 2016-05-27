from src.pqueue import pqueue, INVALID

data = [(5, 'write code'), (7, 'release product'),
        (1, 'write spec'), (3, 'create tests')]
updated_data = [(5, 'write code'), (2, 'release product'),
                (1, 'write spec'), (3, 'create tests')]
sorted_data = [v for (k, v) in sorted(data, key=lambda x: x[0])]
sorted_updated = [v for (k, v) in sorted(updated_data, key=lambda x: x[0])]


def populate_q():
    q = pqueue()
    for item in data:
        q.enqueue(item)
    return q


def dequeues(q):
    while not q.empty():
        yield q.dequeue()


def enqueue():
    q = populate_q()
    assert [v for (k, v) in q.heap] == sorted_data


def dequeue():
    q = populate_q()
    assert list(dequeues(q)) == sorted_data
    assert q.empty()
    assert not q.dequeue()


def update():
    q = populate_q()
    q.update(2, 'release product')
    assert q.size == len(data)
    assert list(dequeues(q)) == sorted_updated


def is_invalid(q, v):
    print q.d
    return v in q.d and INVALID in set(q.d[v])


def has_invalids(q):
    for v in q.d:
        if is_invalid(q, v):
            return True
    return False


def random_updates():
    vals = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
    updates = "c g o a n p".split()
    q = pqueue()
    for k, v in enumerate(vals):
        q.enqueue((k, v))
    for k, v in enumerate(updates):
        q.update((k % 5), v)
    assert len(vals) == q.size
    list(dequeues(q))
    assert not has_invalids(q)
