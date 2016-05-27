# coding: utf-8

# pqueue.py -- an implementation of priority queues using Python's heapq.

# A "decrease key" operation is implemented by marking updated entries but
# otherwise leaving them in the heap until they are found (and removed and
# ignored) by a pop operation. The updated entry is inserted using heappush
# (with the updated priority) to obtain O(log n) update performance.

import heapq

INVALID = '#invalid#'


class pqueue(object):
    def __init__(self, *items):
        self.size = 0
        self.d = dict()
        self.heap = []
        for k, v in items:
            self.enqueue((k, v))

    def enqueue(self, (k, v)):
        "entry is a mutable list to be evnt. modified by `update`"
        self.size += 1
        entry = [k, v]
        self.d[v] = entry
        heapq.heappush(self.heap, entry)

    def __contains__(self, v):
        return v in [x for (_, x) in self.heap]

    def _pop(self):
        k, v = heapq.heappop(self.heap)
        if v != INVALID:
            del self.d[v]
        return k, v

    def dequeue(self):
        if self.empty():
            return None
        k, v = self._pop()
        while v == INVALID:
            k, v = self._pop()
        self.size -= 1
        return v

    def update(self, k, v):
        if v not in self.d:
            self.enqueue((k, v))
            return
        entry = self.d[v]
        entry[1] = INVALID      # modify the reference to the heap entry
        new_entry = [k, v]      # update a mutable list
        self.d[v] = new_entry
        heapq.heappush(self.heap, new_entry)

    def empty(self):
        return self.size == 0
