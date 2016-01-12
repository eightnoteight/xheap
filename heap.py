# -*- coding: utf-8 -*-

"""
Copies from heapq in order to:
1) add remove_by_index -> not as easy as you think
2) add remove_by_item -> heapq does not provide O(log n) for this
3) provide oo implementation
4) comparison is heap-specific (i.e. the same set of items might compare differently on different heaps -> max, min etc.)
5) shorter calls
6) checking invariant
"""

from __future__ import unicode_literals

import heapq


class Heap(list):
    """
    Heap Invariant: a[k] <= a[2*k+1] and a[k] <= a[2*k+2]
    """

    def __init__(self, iterable=[], cmp=lambda x, y: x <= y):
        super(Heap, self).__init__(list(iterable))
        self.cmp = cmp
        self.heapify()

    def push(self, item):
        """Push item onto heap, maintaining the heap invariant."""
        if item in self._indexes:
            raise RuntimeError('same item not allowed to be inserted twice.')
        self.append(item)
        self._siftdown(0, len(self) - 1)

    def pop(self, index=0):
        """Pop item with given index off the heap (default smallest), maintaining the heap invariant."""
        lastelt = super(Heap, self).pop()    # raises appropriate IndexError if heap is empty
        if index == len(self):
            returnitem = lastelt
        else:
            returnitem = self[index]
            self[index] = lastelt
            if not index or self.cmp(self[(index - 1) >> 2], lastelt):
                self._siftup(index)
            else:
                self._siftdown(0, index)
        return returnitem

    def remove(self, item):
        return self.pop(self._indexes.pop(item))

    def replace(self, item):
        """Pop and return the current smallest value, and add the new item.

        This is more efficient than heappop() followed by heappush(), and can be
        more appropriate when using a fixed-size heap.  Note that the value
        returned may be larger than item!  That constrains reasonable uses of
        this routine unless written as part of a conditional replacement:

            if item > heap[0]:
                item = heapreplace(heap, item)
        """
        returnitem = self[0]    # raises appropriate IndexError if heap is empty
        self[0] = item
        self._siftup(0)
        return returnitem

    def pushpop(self, item):
        """Fast version of a heappush followed by a heappop."""
        if self and self.cmp(self[0], item):
            item, self[0] = self[0], item
            self._siftup(0)
        return item

    def check_invariant(self):
        for index in range(len(self)-1, 0, -1):
            parent_index = (index-1) >> 1
            if self.cmp(self[parent_index], self[index]):
                continue
            break
        else:
            return
        raise Exception('heap invariant (heap[{parent_index}] <= heap[{index}]) violated: {parent} !<= {item}'.format(parent=self[parent_index], parent_index=parent_index, item=self[index], index=index))

    def __setitem__(self, key, value):
        self._indexes[value] = key
        super(Heap, self).__setitem__(key, value)

    def __setslice__(self, i, j, sequence):
        super(Heap, self).__setslice__(i, j, sequence)
        self._indexes = {value: index for index, value in enumerate(self)}

    def __repr__(self):
        return 'Heap({content})'.format(content=super(Heap, self).__repr__())

    def _siftdown(*args):
        heapq._siftdown(*args)

    def _siftup(*args):
        heapq._siftup(*args)

    def heapify(self):
        self._indexes = {value: index for index, value in enumerate(self)}
        heapq.heapify(self)


if __name__ == "__main__":
    # Simple sanity test

    heap = Heap([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
    heap.heapify()
    print(heap)
    heap.remove(6)
    heap.remove(2)
    heap.check_invariant()
    print(heap)
    sort = []
    while heap:
        heap.check_invariant()
        sort.append(heap.pop())
    print sort