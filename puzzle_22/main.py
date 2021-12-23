from typing import final
import queue

Coord = tuple[int, int]
Volume = tuple[Coord, Coord, Coord]

def x0(v: Volume) -> int: return v[0][0]
def x1(v: Volume) -> int: return v[0][1]

def y0(v: Volume) -> int: return v[1][0]
def y1(v: Volume) -> int: return v[1][1]

def z0(v: Volume) -> int: return v[2][0]
def z1(v: Volume) -> int: return v[2][1]

class Cube():
    def __init__(self, action, x, y, z) -> None:
        self.action = 0 if action == 'off' else 1
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self) -> str:
        return '{} -> {}, {}, {}'.format(self.action, self.x, self.y, self.z)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def as_volume(self) -> Volume:
        return (self.x, self.y, self.z)

def read_line(line: str):
    action, rest = line.strip().split(' ')
    xyz = [tuple([int(s) for s in c[2:].split('..')]) for c in rest.split(',')]
    return Cube(action, xyz[0], xyz[1], xyz[2])

cubes = [read_line(l) for l in open('input.txt', 'r')]

# FOR PART 1
dim = 101
field = [0] * dim * dim * dim
def set_cube(field: list[int], cube: Cube):
    x1, x2 = cube.x
    y1, y2 = cube.y
    z1, z2 = cube.z
    mx = x2 - x1

    def clamp(v, mi=-50, ma=50): 
        return max(min(v, ma), mi)

    def check(a, b):
        if a > 50 or b < -50: return False, False
        assert b - a >= 0
        return clamp(a), clamp(b)

    x1, x2 = check(x1, x2)
    if x1 == False: return
    y1, y2 = check(y1, y2)
    if y1 == False: return
    z1, z2 = check(z1, z2)
    if z1 == False: return

    fill = [cube.action] * (mx + 1)
    for z in range((z1 + 50) * dim*dim, (z2 + 50) * dim*dim + 1, dim*dim):
        for y in range((y1 + 50) * dim, (y2 + 50 + 1) * dim, dim):
            offset = y + z + 50
            field[x1 + offset : x2 + offset + 1] = fill

# PART 1
for c in cubes:
    set_cube(field, c)

# PART 1
print(field.count(1))

def intersect_cubes(cube1: Volume, cube2: Volume) -> Volume:
    def intersect_axis(cube1axis: Coord, cube2axis: Coord) -> Coord:
        return (
            max(cube1axis[0], cube2axis[0]), # => cube2axis[0] if cube1axis[0] < cube2axis[0] else cube1axis[0]
            min(cube1axis[1], cube2axis[1])  # => cube2axis[1] if cube2axis[1] < cube1axis[1] else cube1axis[1]
        )
    
    if x1(cube1) < x0(cube2) or \
       x1(cube2) < x0(cube1) or \
       y1(cube1) < y0(cube2) or \
       y1(cube2) < y0(cube1) or \
       z1(cube1) < z0(cube2) or \
       z1(cube2) < z0(cube1): return None # No intersection

    return (
        intersect_axis(cube1[0], cube2[0]),
        intersect_axis(cube1[1], cube2[1]),
        intersect_axis(cube1[2], cube2[2])
    )

def volume(v: Volume) -> int:
    return (x1(v) - x0(v) + 1) * (y1(v) - y0(v) + 1) * (z1(v) - z0(v) + 1)

def subtract_intersection(cube: Volume, intersection: Volume) -> list[Volume]:

    # +------+
    # |L TT R|
    # |L    R|
    # |L BB R|
    # +------+
    # R  = right side
    # L  = left  side
    # TT = top   side
    # BB = botto side

    result = []

    if x0(cube) != x0(intersection):
        leftSide = (
            (x0(cube), x0(intersection) - 1),
            cube[1],
            cube[2]
        )
        result.append(leftSide)

    if x1(cube) != x1(intersection):
        rightSide = (
            (x1(intersection) + 1, x1(cube)),
            cube[1],
            cube[2]
        )
        result.append(rightSide)

    if y0(cube) != y0(intersection):
        bottomSide = (
            intersection[0],
            (y0(cube), y0(intersection) - 1),
            cube[2]
        )
        result.append(bottomSide)

    if y1(cube) != y1(intersection):
        topSide = (
            intersection[0],
            (y1(intersection) + 1, y1(cube)),
            cube[2]
        )
        result.append(topSide)

    if z0(cube) != z0(intersection):
        centerBottomSide = (
            intersection[0],
            intersection[1],
            (z0(cube), z0(intersection) - 1)
        )
        result.append(centerBottomSide)

    if z1(cube) != z1(intersection):
        centerTopSide = (
            intersection[0],
            intersection[1],
            (z1(intersection) + 1, z1(cube))
        )
        result.append(centerTopSide)
    
    return result

def subtract_volume(to_subtract: Volume, volumes: list[Volume]) -> tuple[int, int]:
    not_yet_checked = queue.SimpleQueue()
    explodes, fragment_volumes = 0, 0
    
    # All existing volumes have to be checked for an intersection
    for x in volumes:
        not_yet_checked.put(x)
    
    # rebuild list later
    volumes.clear()

    # Check for each volume (all these do NOT overlap) ...
    while not not_yet_checked.empty():
        # Get next volume to check for intersection
        next_volume = not_yet_checked.get()
        # .. if `to_subtract` intersects, if so, throw away intersection and keep the rest
        intersection = intersect_cubes(to_subtract, next_volume)
        if intersection:
            difference = subtract_intersection(next_volume, intersection)
            explodes += 1
            fragment_volumes += len(difference)
            volumes.extend(difference)
        else:
            volumes.append(next_volume)

    return explodes, fragment_volumes

def integrate_volume(to_integrate: Volume, volumes: list[Volume]) -> tuple[int, int]:
    not_integrated_yet = queue.SimpleQueue()
    not_integrated_yet.put(to_integrate)
    explodes, fragment_volumes = 0, 0

    # Until there are volumes not integrated (ones that have not been checked for collisions)
    while not not_integrated_yet.empty():
        # Get next such volume
        next_volume = not_integrated_yet.get()
        # Assume there are no collisions
        no_collisions = True
        # Check for each already integrated volume (all these do NOT overlap) ...
        for x in volumes:
            # .. if the `next_volume` intersects (= collides)
            intersection = intersect_cubes(next_volume, x)
            if intersection:
                # print('intersection', intersection)
                # ... explode `next_volume` (= make it smaller) ...
                difference = subtract_intersection(next_volume, intersection)
                explodes += 1
                fragment_volumes += len(difference)
                no_collisions = False
                # ... and schedule the smaller parts again
                # This repeats until a volumes does not collide with any already integrated volume
                for d in difference: not_integrated_yet.put(d)
                
                # if we found a collision, we should not search further collisions!
                break
            
        # if `next_volume` does not collide with any already integrated volume
        # we can integrate it!
        if no_collisions: volumes.append(next_volume)

    return explodes, fragment_volumes


# PART 2   
intersections = 0
final_volumes = []
g_explodes, g_fragment_volumes = 0, 0

for icube, cube in enumerate(cubes):
    cube_volume = cube.as_volume()
    # skip offs for now
    if cube.action == 0:
        explodes, fragment_volumes = subtract_volume(cube_volume, final_volumes)
    else:
        explodes, fragment_volumes = integrate_volume(cube_volume, final_volumes)
    g_explodes += explodes
    g_fragment_volumes += fragment_volumes
    print('Done with cube #{} of {} [explodes: {}, fragments: {}]'.format(icube + 1, len(cubes[1:]), g_explodes, g_fragment_volumes))

on_count = sum([volume(v) for v in final_volumes])
print(on_count)