import functools


lines = [x.strip() for x in open('input.txt', 'r')]

def is_opening(c):
    return c in ['(', '[', '{', '<']

def opposite(c):
    return {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }[c]

def get_score(c):
    return {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }[c]

def line_corrupted(line):
    stack = []
    for c in line:
        if is_opening(c):
            stack.append(c)
        elif c != opposite(stack.pop()):
            return (True, c)
    return (False, stack)

# PART 1

print(sum([get_score(line_corrupted(x)[1]) for x in lines if line_corrupted(x)[0] != False]))

# PART 2

def get_score_2(c):
    return {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4,
    }[c]

def calc_score(stack: list[str]):
    stack.reverse()
    return functools.reduce(lambda a, b: a * 5 + get_score_2(b), stack, 0)

incomplete = [line_corrupted(x)[1] for x in lines if not line_corrupted(x)[0]]
scores = [calc_score(i) for i in incomplete]
scores.sort()
print(scores[int(len(scores) / 2)])