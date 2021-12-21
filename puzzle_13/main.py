from typing import Coroutine


def read_input():
    lines = list([x.strip() for x in open('input.txt', 'r')])

    dot_coords = []
    instructions = []

    read_instructions = False
    for l in lines:
        if l == '':
            read_instructions = True
            continue
        elif read_instructions:
            i = l.split(' ')[2].split('=')
            instructions.append((i[0], int(i[1])))
        else:
            c = l.split(',')
            dot_coords.append((int(c[0]), int(c[1])))
    
    return dot_coords, instructions

dot_coords, instructions = read_input()

def fold(coords, instruction):
    new_coords = set([])
    axis, num = instruction
    if axis == 'y':
        for (x, y) in coords:
            if y > num:
                new_coords.add((x, 2 * num - y))
            else:
                new_coords.add((x, y))
    else:
        for (x, y) in coords:
            if x > num:
                new_coords.add((2 * num - x, y))
            else:
                new_coords.add((x, y))
    return new_coords

for i in instructions:
    dot_coords = fold(dot_coords, i)

print (dot_coords)
def visualize(coords):
    width = max([x for (x, y) in coords]) + 1
    height = max([y for (x, y) in coords]) + 1
    pos = [x + y * width for (x, y) in coords]
    pos.sort(reverse=True)
    s = ''
    for y in range(height):
        for x in range(width):
            if len(pos) > 0 and pos[-1] == (x + y * width):
                pos.pop()
                s = s + '#'
            else:
                s = s + ' '
        s = s + '\n'
    print(len(pos))
    return s

print(visualize(dot_coords))