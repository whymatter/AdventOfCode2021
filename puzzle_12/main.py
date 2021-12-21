import functools


lines = list([x.strip().split('-') for x in open('input.txt', 'r')])

x = {}
for (s, e) in lines:
    t = x.get(s, set([]))
    t.add(e)
    x[s] = t
    
    t = x.get(e, set([]))
    t.add(s)
    x[e] = t

def is_big(x: str):
    return x == x.upper()

def is_small(x: str):
    return not is_big(x)

def abort_puzzle_2(path, new):
    if new == 'start' and new in path:
        return True
    
    if new not in path or is_big(new):
        return False

    all_small = set([n for n in path if is_small(n)])
    for s in all_small:
        if path.count(s) > 1:
            return True
    
    return False

def depth_first(m: dict[str, set[str]], node: str, path: list[str], found_paths: list[str]):
    if abort_puzzle_2(path, node):
        return

    path.append(node)
    if node == 'end':
        found_paths.append(path.copy())
        path.pop()
        return

    adj: set[str] = x.get(node)
    for a in adj:
        depth_first(m, a, path, found_paths)
    
    path.pop()

found = []
depth_first(x, 'start', [], found)

for f in found:
    print(f)

print(len(found))