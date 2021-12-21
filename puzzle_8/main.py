import functools
from os import error, popen, remove

def split_line(l):
    return [x.strip().split(' ') for x in l.split('|')]

lines = [split_line(x.strip()) for x in open('input.txt', 'r')]

r = [e for l in lines for e in l[1] if len(e) in [2, 3, 4, 7]]

print(len(r))

def get_n(x, n):
    return [list(y) for y in x if len(y) == n]

def get_all():
    return {
        c: [x for x in ['a', 'b', 'c', 'd', 'e', 'f', 'g']] for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    }

def remove_all(l, *args):
    for i in args:
        if i in l:
            l.remove(i)

def decode(l):
    first, second = l
    possibilities = get_all()

    _1 = get_n(first, 2)[0]
    for c in possibilities.keys():
        if c in _1:
            remove_all(possibilities[c], 'a', 'b', 'd', 'e', 'g')
        else:
            remove_all(possibilities[c], 'c', 'f')
    # print(possibilities)

    _4 = get_n(first, 4)[0]
    for c in possibilities.keys():
        if c in _4 and c not in _1:
            remove_all(possibilities[c], 'a', 'c', 'e', 'f', 'g')
        elif c not in _4:
            remove_all(possibilities[c], 'b', 'c', 'd', 'f')
    # print(possibilities)

    _7 = get_n(first, 3)[0]
    for c in possibilities.keys():
        if c in _7 and c not in _1:
            remove_all(possibilities[c], 'b', 'c', 'd', 'e', 'f', 'g')
        elif c not in _7:
            remove_all(possibilities[c], 'a', 'c', 'f')
    # print(possibilities)

    _6er = get_n(first, 6)
    if all([_1[0] in l for l in _6er]):
        remove_all(possibilities[_1[0]], 'c')
        remove_all(possibilities[_1[1]], 'f')
    elif all([_1[1] in l for l in _6er]):
        remove_all(possibilities[_1[0]], 'f')
        remove_all(possibilities[_1[1]], 'c')
    else:
        raise error("first")
    # print(possibilities)
    
    in_4_but_not_1 = list(set(_4) - set(_1))
    if all([in_4_but_not_1[0] in l for l in _6er]):
        remove_all(possibilities[in_4_but_not_1[0]], 'd')
        remove_all(possibilities[in_4_but_not_1[1]], 'b')
    elif all([in_4_but_not_1[1] in l for l in _6er]):
        remove_all(possibilities[in_4_but_not_1[0]], 'b')
        remove_all(possibilities[in_4_but_not_1[1]], 'd')
    else:
        raise error("in_4_but_not_1")
    # print(possibilities)

    not_in_4_and_7 = list(set(['a', 'b', 'c', 'd', 'e', 'f', 'g']) - set(_4 + _7))
    if len([x for x in first if not_in_4_and_7[0] in x]) == 7:
        remove_all(possibilities[not_in_4_and_7[0]], 'e')
        remove_all(possibilities[not_in_4_and_7[1]], 'g')
    elif len([x for x in first if not_in_4_and_7[1] in x]) == 7:
        remove_all(possibilities[not_in_4_and_7[0]], 'g')
        remove_all(possibilities[not_in_4_and_7[1]], 'e')
    else:
        raise error("not_in_4_and_7")
    # print(possibilities)

    def translate(x):
        if x == set(['a', 'b', 'c', 'e', 'f', 'g']): return 0
        if x == set(['c', 'f']): return 1
        if x == set(['a', 'c', 'd', 'e', 'g']): return 2
        if x == set(['a', 'c', 'd', 'f', 'g']): return 3
        if x == set(['b', 'c', 'd', 'f']): return 4
        if x == set(['a', 'b', 'd', 'f', 'g']): return 5
        if x == set(['a', 'b', 'd', 'e', 'f', 'g']): return 6
        if x == set(['a', 'c', 'f']): return 7
        if x == set(['a', 'b', 'c', 'd', 'e', 'f', 'g']): return 8
        if x == set(['a', 'b', 'c', 'd', 'f', 'g']):return 9

        raise error(x)
    
    result = ""
    for num in second:
        result = result + str(translate(set([possibilities[x][0] for x in num])))
    return int(result)

total = 0
for x in lines:
    total = total + decode(x)
print(total)