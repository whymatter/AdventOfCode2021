import functools

# PART 1

lines = [x.strip() for x in list(open('input.txt', 'r'))]
line_length = len(lines[0])
num_lines = len(lines)

def as_num_list(line):
    return [int(x) for x in line]

def vector_add(a, b):
    return [x + b[xi] for xi, x in enumerate(a)]

def bin_to_dec(x):
    return sum([pow(2, ia) for ia, a in enumerate(x[::-1]) if a == 1])

bit_sum = functools.reduce(lambda a, b: vector_add(a, as_num_list(b)), lines, [0]*line_length)

most_common_bits = [int(x > (num_lines - x)) for x in bit_sum]
least_common_bits = [int(x < (num_lines - x)) for x in bit_sum]

gamma = bin_to_dec(most_common_bits)
epsilon = bin_to_dec(least_common_bits)

print(gamma, epsilon, gamma * epsilon)

# PART 2

def calc_bit_sum(all):
    return functools.reduce(lambda a, b: vector_add(a, b), all, [0]*line_length)

def keep_lines(all, index, search_value):
    return [x for x in all if x[index] == search_value]

def find(common_func):
    remaining = [as_num_list(x) for x in lines]
    for i in range(line_length):
        bit_sum = calc_bit_sum(remaining)
        most_common = int(common_func(bit_sum[i], (len(remaining) - bit_sum[i])))
        remaining = [x for x in remaining if x[i] == most_common]
        if (len(remaining) == 1):
            break

    if len(remaining) != 1:
        raise "rem not len 1"

    return bin_to_dec(remaining[0])

oxy = find(lambda a, b: a >= b)
co2 = find(lambda a, b: a < b)

print(oxy, co2, oxy * co2)