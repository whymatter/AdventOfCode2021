import functools

min_x, max_x, min_y, max_y = 175, 227, -134, -79
# min_x, max_x, min_y, max_y = 20, 30, -10, -5

possible_vx0s = []
possible_vy0s = []

def hits_x(s, v, min_x, max_x):
    """Calculates all possible hits = array """

    # abort if we cant event reach min_x
    if (v * v + v) / 2 < min_x: return []

    steps = []

    # if v0 gets 0, we cant move forward neither score new hits
    for step in range(v):
        s += v
        v = max(0, v - 1)

        # if hit -> save hit
        if s >= min_x and s <= max_x:
            steps.append((step + 1, v)) # we start counting steps at 1
                                        # also save velocity on hit
        # if we start to leave the target area ...
        elif s > max_x:
            # ... we are done
            break
            
    return steps

def hits_y(s0, v0, min_y, max_y):
    while True:
        s0 += v0
        v0 -= 1
        if s0 >= min_y and s0 <= max_y:
            return True
        elif s0 > max_y:
            return False

# calculate all possible x velocities
v0 = 1
# xVelocity cannt be larger than max_x (otherwise we miss the target are on the first step)
while v0 <= max_x:
    hits = hits_x(0, v0, min_x, max_x)
    if len(hits) > 0:
        possible_vx0s.append((v0, hits))
    v0 += 1

steps = functools.reduce(lambda a,b: [*a, *b[1]], possible_vx0s, [])
steps = set(steps)

possible_x_velocities = functools.reduce(lambda a,b: [*a, b[0]], possible_vx0s, [])
possible_x_velocities = set(possible_x_velocities)

# v0 = 1
# while True:
#     if hits_y(0, v0, min_y, max_y):
#         possible_vy0s.append(v0)
#     elif len(possible_vy0s) > 0: 
#         break
#     v0 += 1

# PART 1:
# We have to shoot the probe into the air.
# Since the gravity slows down the probe with the same acceleration as it accelerates the probe
# The velocity of the probe will pass the x axis exactly at y = 0
# The max velocity the probe can have at y=0 is max_x
# Therefore the starting velocity was max_x-1
# The highest point is then calculated by the sum formular (n*n+n)/2

# PART 2:
# We have to consider the following cases:
#  - All hits_x where xVelocity > 0
#  - (All hits_x where xVelocity = 0) * (possible y locations)


initial_velocities = set()

for (xV0, steps) in possible_vx0s:
    for (s, v) in steps:

        if v == 0:
            for yV0 in range(1, -min_y):
                for s2 in range(s, 2 * yV0 + abs(min_y)):
                    y1 = int((yV0 * yV0 + yV0) / 2)
                    steps_down = s2 - yV0 - 1
                    y2 = y1 - int((steps_down * steps_down + steps_down) / 2)
                    if y2 >= min_y and y2 <= max_y:
                        initial_velocities.add((xV0, yV0))
        
            for yV0 in range(min_y, 1):
                for s2 in range(s, -min_y * 2):
                    y2 = int(-((s2-1)**2 + s2 - 1)/2 + yV0*s2)
                    if y2 >= min_y and y2 <= max_y:
                        initial_velocities.add((xV0, yV0))


        # print(xV0, s, v, max_v_y)

        # Hit ocured at step=s, calculate possible positive yVelocities
        for yV0 in range(1, s):
            y1 = int((yV0 * yV0 + yV0) / 2)
            steps_down = s - yV0 - 1
            y2 = y1 - int((steps_down * steps_down + steps_down) / 2)
            # if xV0 == 7 and v == 0:
            #     print(yV0, y1, steps_down, y2)
            if y2 >= min_y and y2 <= max_y:
                initial_velocities.add((xV0, yV0))
        
        for yV0 in range(min_y, 1):
            y2 = int(-((s-1)**2 + s - 1)/2 + yV0*s)
            if y2 >= min_y and y2 <= max_y:
                initial_velocities.add((xV0, yV0))

            # 11+12+13
            # 1+10+2+10+3+10
            # 1+2+3+10*3
# print(possible_x_velocities)
print(initial_velocities)
print("Len", len(initial_velocities))
# print(possible_vy0s)