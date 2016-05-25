
# pqueue.py -- an implementation of priority queues using Python's heapq.

# A "decrease key" operation is implemented by marking updated entries but
# otherwise leaving them in the heap until they are found (and removed and
# ignored) by a pop operation.  The updated entry is inserted using heappush
# (with the updated priority) to obtain O(log n) update performance.

import heapq
from collections import defaultdict

INVALID = '#invalid#'


class pqueue(object):
    def __init__(self, *items):
        self.size = 0
        self.d = defaultdict(dict)
        self.heap = []
        for k, v in items:
            self.enqueue((k, v))

    def enqueue(self, (k, v)):
        self.d[v][k] = v
        self.size += 1
        heapq.heappush(self.heap, (k, v))

    def __contains__(self, v):
        return v in self.d

    def _pop(self):
        k, v = heapq.heappop(self.heap)
        while k in self.d[v] and self.d[v][k] == INVALID:
            del self.d[v][k]
            try:
                k, v = heapq.heappop(self.heap)
            except IndexError:
                return
        return k, v

    def dequeue(self):
        item = self._pop()
        if item:
            self.size -= 1
            k, v = item
            return v

    def update(self, k, v):
        if v not in self:
            self.enqueue((k, v))
            return
        ks = self.d[v].keys()
        assert len(ks) == 1
        self.d[v][ks[0]] = INVALID
        heapq.heappush(self.heap, (k, v))

    def empty(self):
        return self.size == 0


# demonstrate usage

def main():
    q = pqueue()
    q.enqueue((5, 'write code'))
    q.enqueue((7, 'release product'))
    q.enqueue((1, 'write spec'))
    q.enqueue((3, 'create tests'))
    print(q.heap)
    print(q.dequeue())
    print(q.heap)
    q.update(2, 'release product')
    print(q.heap)
    print(q.dequeue())
    q.update(1, 'write code')
    print(q.heap)
    print(q.dequeue())
    print(q.heap)
    print(q.dequeue())
    print(q.heap)
    print(q.dequeue())
    print(q.size)
    print(q.heap)

if __name__ == '__main__':
    main()
