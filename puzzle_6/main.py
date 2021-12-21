import functools

fish = [int(x) for x in open('input.txt', 'r').read().split(',')]
fishMap = {i:0 for i in range(9)}

for f in fish:
    fishMap[f] = fishMap[f] + 1

def day_of_a_fish_in_map(fishMap):
    fishMap[0], fishMap[1], fishMap[2], fishMap[3], fishMap[4], fishMap[5], fishMap[6], fishMap[7], fishMap[8] = \
    fishMap[1], fishMap[2], fishMap[3], fishMap[4], fishMap[5], fishMap[6], fishMap[7] + fishMap[0], fishMap[8], fishMap[0]

# PART 1
def day_of_a_fish(fish):
    l = len(fish)
    for i in range(l):
        fish[i] = fish[i] - 1
        if fish[i] == -1:
            fish[i] = 6
            fish.append(8)

for days in range(256):
    day_of_a_fish_in_map(fishMap)
    print(fishMap, sum(fishMap.values()))

print(sum(fishMap.values()))