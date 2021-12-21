lines = [x.strip() for x in open('input.txt', 'r')]

padding = 2

coding = lines[0].replace('#', '1').replace('.', '0')
image = ["0" * padding + l.replace('#', '1').replace('.', '0') + "0" * padding for l in lines[2:]]
image = [*["0" * len(image[0]) for _ in range(padding)], *image, *["0" * len(image[0]) for _ in range(padding)]]

def get_index(image, x, y):
    s = image[y-1][x-1:x+2] + image[y][x-1:x+2] + image[y+1][x-1:x+2]
    return int(s, 2)

def get_new(image, c, padding = 0):
    new_image = [
        *[c * (len(image[0]) + padding*2-2) for _ in range(padding)]
    ]

    for y in range(1, len(image) - 1):
        new_image.append(c * padding)
        for x in range(1, len(image[0]) - 1):
            i = get_index(image, x, y)
            new_image[-1] += coding[i]
        new_image[-1] += c * padding
    
    for _ in range(padding):
        new_image.append(c * (len(image[0]) + padding*2-2))

    return new_image
    
c = 0
for l in get_new(get_new(image, '1', 2), '0', 0):
    c += l.count('1')
print(c)

for i in range(25):
    image = get_new(image, '1', 2)
    image = get_new(image, '0', 2)

c = 0
for l in image:
    c += l.count('1')
print(c)