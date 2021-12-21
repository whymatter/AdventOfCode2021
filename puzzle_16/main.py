import binascii
import functools

text = open('input.txt', 'r').read().strip()

trans = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

binary = functools.reduce(lambda a,b: a + trans[b], text, "")

def to_string(data, start, length):
    return "".join(data[start:start+length]), start + length

def to_number(data, start, length):
    s, start = to_string(data, start, length)
    return int(s, 2), start

def read_packet(data, start):
    version, start = to_number(data, start, 3)
    typeId, start = to_number(data, start, 3)

    print("Version/TypeId", version, typeId)

    if typeId == 4:
        value, start = read_literal(data, start)
        print("Literal", value)
        return (version, typeId, value), start
    else:
        sub_packets, start = read_operator(data, start)
        return (version, typeId, sub_packets), start

def read_literal(data, start):
    value = ""
    
    while True:
        leading_bit, start = to_number(data, start, 1)
        tmp, start = to_string(data, start, 4)
        value += tmp
        if leading_bit == 0: break

    return to_number(value,0,len(value))[0], start

def read_operator(data, start):
    length_type_id, start = to_number(data, start, 1) # 0 => The next 15 bits are a number that represents the total length in bits
                                                      # 1 => The next 11 bits are a number that represents the number of sub-packets
    if length_type_id == 0:
        return read_operator_0(data, start)
    else:
        return read_operator_1(data, start)

def read_operator_0(data, start):
    length_in_bits, start = to_number(data, start, 15)
    print("Operator [0]", length_in_bits)
    end = start + length_in_bits
    packets = []
    while start != end:
        packet, start = read_packet(data, start)
        packets.append(packet)
    return packets, start

def read_operator_1(data, start):
    num_sub_packets, start = to_number(data, start, 11)
    print("Operator [1]", num_sub_packets)
    packets = []
    for _ in range(num_sub_packets):
        packet, start = read_packet(data, start)
        packets.append(packet)
    return packets, start

result, start = read_packet(binary, 0)
print(result)

def count_version(packet):
    count = packet[0]

    if packet[1] == 4: return count # if literal, no further counting
    
    # else count all sub packets
    for p in packet[2]:
        count += count_version(p)
    return count

print(count_version(result))

def calculate(packet):
    _, type, val = packet
    if type == 0:
        return sum([calculate(x) for x in val])
    elif type == 1:
        return functools.reduce(lambda a,b: a * calculate(b), val, 1)
    elif type == 2:
        return min([calculate(x) for x in val])
    elif type == 3:
        return max([calculate(x) for x in val])
    elif type == 4:
        return val
    elif type == 5:
        return (1 if calculate(val[0]) > calculate(val[1]) else 0)
    elif type == 6:
        return (1 if calculate(val[0]) < calculate(val[1]) else 0)
    elif type == 7:
        return (1 if calculate(val[0]) == calculate(val[1]) else 0)
    else:
        print('Invalid type', type)

print(calculate(result))