from collections import Counter
import string

lines = [x.strip() for x in open('input.txt', 'r')]

template = lines[0]

rules = {x.split(' -> ')[0]:x.split(' -> ')[1] for x in lines[2:]}

# def run_insertation(template, rules):
#     result = template[0]
#     for i, c in enumerate(template[1:]):
#         result = result + rules[template[i] + c] + c
#     return result

# for _ in range(10):
#     template = run_insertation(template, rules)

# freq = [template.count(c) for c in string.ascii_uppercase if c in template]
# mi = min(freq)
# ma = max(freq)
# print(mi, ma, ma-mi)

# PART 2

global_count = {c:0 for c in string.ascii_uppercase}
leafs = {(k[0], k[1]):((k[0], v), (v, k[1])) for (k, v) in rules.items()}

def count(template, iter=10):
    cnt = Counter()
    for i in range(len(template) - 1):
        cnt[tuple(template[i:i+2])] += 1
        
    for _ in range(iter):
        items = list(cnt.items())
        cnt = Counter()
        for (pair, num) in items:
            l1, l2 = leafs[pair]
            cnt[l1] += num
            cnt[l2] += num            
            
    cnt2 = Counter()
    for (k, v) in cnt.items():
        cnt2[k[0]] += v
        cnt2[k[1]] += v
    cnt2[template[0]] += 1
    cnt2[template[-1]] += 1
    print((max(cnt2.values()) - min(cnt2.values()))/2)

count(template, 10)
count(template, 40)