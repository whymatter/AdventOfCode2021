import functools

# PART 1

positions = [int(x) for x in open('input.txt', 'r').read().split(',')]

_min = min(positions)
_max = max(positions)

min_fuel = _max * len(positions)
for i in range(_min, _max + 1):
    min_fuel = min(sum([abs(p - i) for p in positions]), min_fuel)

print(min_fuel)

# PART 2

min_fuel = 0.5 * _max * len(positions) * (_max * len(positions) + 1)
for i in range(_min, _max + 1):
    min_fuel = min(sum([0.5 * abs(p - i) * (abs(p - i) + 1) for p in positions]), min_fuel)

print(int(min_fuel))