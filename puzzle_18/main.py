import itertools
import numbers

def to_list(number, depth=0):
    if isinstance(number, numbers.Number): return [(number, depth)]
    a, b = number
    return [*to_list(a, depth=depth+1), *to_list(b, depth=depth+1)]

numbers = [to_list(eval(x.strip())) for x in open('input.txt', 'r')]

def add(a, b):
    a = [(v, d+1) for (v, d) in a]
    b = [(v, d+1) for (v, d) in b]
    return [*a, *b]

def explode(number: list, i=0):
    while i < (len(number) - 1):
        v, d = number[i]
        if d == 5:
            if i > 0:
                lv, ld = number[i-1]
                number[i-1] = (lv + v, ld)
            if i+2 < len(number):
                v2, _ = number[i+1]
                rv, rd = number[i+2]
                number[i+2] = (rv + v2, rd)
            number[i] = (0, d-1)
            del number[i+1]
        i += 1
    return number

def split(number: list, i=0):
    while i < len(number):
        v, d = number[i]
        if v >= 10:
            l = int(v / 2)
            r = v - l            
            number[i] = (l, d+1)
            number.insert(i+1, (r, d+1))
            # if we created an entry with depth 5, then run explode starting from that position
            if d == 4: explode(number, i)
            i = -1
        i += 1
    return False

def reduce(number: list):
    # we start with explode
    explode(number)
    # split will return if nothing left to split or explode
    split(number)

    return number

def magnitude(number):
    for c in range(4, 0, -1):
        result2, i = [], 0
        while i < len(number):
            v,d = number[i]
            if d == c:
                result2.append((v*3+number[i+1][0]*2, d-1))
                i += 2
            else:
                result2.append(number[i])
                i += 1
        number, result2 = result2, number
    return number[0][0]

# PART 1

result = numbers[0]
for i in range(1, len(numbers)):
    result = add(result, numbers[i])
    result = reduce(result)

print(magnitude(result))

# PART 2

max_mag = 0
for p in itertools.permutations(numbers, 2):
    result = add(p[0], p[1])
    result = reduce(result)
    m = magnitude(result)
    max_mag = max(max_mag, m)

print(max_mag)