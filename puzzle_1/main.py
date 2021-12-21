import functools
import itertools
import collections

# PART 1

lines = [int(x.strip()) for x in list(open('input.txt', 'r'))]

print(functools.reduce(lambda a, b: (a[0] + (1 if a[1] < b else 0), b), lines, (0, 0))[0] - 1)

# PART 2

def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)

windowed = map(lambda a: sum(a), sliding_window(lines, 3))

print(functools.reduce(lambda a, b: (a[0] + (1 if a[1] < b else 0), b), windowed, (0, 0))[0] - 1)