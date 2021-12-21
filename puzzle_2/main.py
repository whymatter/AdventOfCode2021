import functools

# PART 1

lines = [(x.split(' ')[0], int(x.split(' ')[1])) for x in list(open('input.txt', 'r'))]

result = functools.reduce(
    lambda a, b: (
        a[0] + (b[1] if b[0] == 'forward' else 0),
        a[1] + (b[1] if b[0] == 'down' else -b[1] if b[0] == 'up' else 0))
    , lines, (0, 0))

print(result[0] * result[1])

# PART 2

result = functools.reduce(
    lambda a, b: (
        a[0] + (b[1] if b[0] == 'forward' else 0),
        a[1] + (((a[2] + (b[1] if b[0] == 'down' else -b[1] if b[0] == 'up' else 0)) * b[1]) if b[0] == 'forward' else 0),
        a[2] + (b[1] if b[0] == 'down' else -b[1] if b[0] == 'up' else 0)
    ) , lines, (0, 0, 0))

print(result[0] * result[1])