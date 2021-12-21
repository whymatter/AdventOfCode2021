import queue
from typing import Hashable, Set
import hashlib

lines = [x.strip() for x in open('input.txt', 'r')]
rows, cols = len(lines), len(lines[0])

nums = [int(y) for x in lines for y in x]

def val(x, y):
    if x < 0 or x >= cols or y < 0 or y >= rows:
        return 10
    return nums[y * cols + x]

total = 0
lows = []

for y in range(rows):
    for x in range(cols):
        if min(val(x-1, y), val(x+1,y), val(x,y-1), val(x,y+1)) > val(x, y):
            total = total + 1 + val(x, y)
            lows.append((x, y))

print(total)

def breadth_first(sx, sy):
    fifo: queue.Queue = queue.SimpleQueue()
    visited: Set = set()

    fifo.put((sx, sy))

    while not fifo.empty():
        x, y = fifo.get()
        visited.add((x, y))

        anchestors = [
            (x2, y2) for x2, y2 in 
            [(x-1, y), (x+1,y), (x,y-1), (x,y+1)] 
            if val(x2, y2) < 9 and val(x2, y2) > val(x, y) and not (x2, y2) in visited
        ]
        
        for a in anchestors:
            fifo.put(a)
            visited.add(a)
    return len(visited)
    
    
r = [breadth_first(l[0], l[1]) for l in lows]
r.sort()
print(r[-1] * r[-2] * r[-3])