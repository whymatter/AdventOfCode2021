import re
import functools

# PART 1 (PART 2 maked below)

def to_line(i):
    match = re.match("(\d+),(\d+) -> (\d+),(\d+)", i)
    return ((int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4))))

def reducer(interpolation):
    def reduce(a: dict[tuple[int, int], int], b: tuple[tuple[int, int], tuple[int,int]]):
        for p in interpolation(b[0], b[1]):
            a[p] = a.get(p, 0) + 1
        return a

    return reduce

def interpol(start: tuple[int, int], end: tuple[int, int]):
    (sx, sy), (ex, ey) = start, end
    if sx == ex:
        return [(sx, y) for y in range(min(sy, ey), max(sy, ey) + 1)]
    elif sy == ey:
        return [(x, sy) for x in range(min(sx, ex), max(sx, ex) + 1)]
    else:
        # PART 2
        return [(sx + (i if sx < ex else -i), sy + (i if sy < ey else -i)) for i in range(abs(sx - ex) + 1)]

print(interpol((10, 2), (5, 2)))
print(interpol((2, 10), (2, 5)))
print(interpol((3, 2), (6, 5)))

lines = [to_line(l) for l in list(open('input.txt', 'r'))]
counts = functools.reduce(reducer(interpol), lines, dict({}))
num = functools.reduce(lambda a, b: a + (1 if b > 1 else 0), counts.values(), 0)

print(num)