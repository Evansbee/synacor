from itertools import permutations
for p in permutations([2,3,5,7,9],5):
    if p[0] + p[1] * p[2]**2 + p[3]**3 - p[4] == 399:
        print(p)
        break