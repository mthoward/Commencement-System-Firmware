""" scanner/Queue.py
Queue wrapper on deque for simplification
"""

# Standard imports
from collections import deque

class Queue(deque):
    def push(self, item):
        self.append(item)

    def pop(self):
        return self.popleft()

    def appendleft(self, item):
        raise AttributeError("'Queue' object has no attribute 'appendleft'")
