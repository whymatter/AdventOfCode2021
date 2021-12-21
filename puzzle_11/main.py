import functools
import itertools
import queue

lines = [x.strip() for x in open('input.txt', 'r')]
rows, cols = len(lines), len(lines[0])
nums = [int(y) for x in lines for y in x]

def val(input, x, y):
    return input[y * cols + x]

def set_val(input, x, y, v):
    input[y * cols + x] = v

def adja_coord(x, y):
    return [
        (xi, yi)
        for xi in range(x-1, x+2) if xi >= 0 and xi < cols
        for yi in range(y-1, y+2) if yi >= 0 and yi < rows and not (xi == x and yi == y)
    ]

def step(input):
    flashed = set([])
    to_flash = queue.SimpleQueue()
    
    for y in range(rows):
        for x in range(cols):
            new_v = val(input, x, y) + 1
            set_val(input, x, y, new_v)
            if new_v > 9:
                to_flash.put((x, y))
    
    while not to_flash.empty():
        p = to_flash.get()
        if p not in flashed:
            flashed.add(p)
            for (ax, ay) in adja_coord(p[0], p[1]):
                new_v = val(input, ax, ay) + 1
                set_val(input, ax, ay, new_v)
                if new_v > 9:
                    to_flash.put((ax, ay))

    output = list(map(lambda a: 0 if a > 9 else a, input))
    return output, len(flashed)

total = 0
for i in range(10000):
    nums, l = step(nums)
    total = total + l
    if all([x == 0 for x in nums]):
        print(i + 1)
        break

print(total)