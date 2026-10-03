from functools import *
import sys
sys.setrecursionlimit(10000)
# @lru_cache(10000)
def F(n):
    if n < 3:        return n + 1
    if n%2==0 and n>999: return 1000
    if n % 2 == 0:   return n + 2 * F(n + 2)
    return F(n - 2) + n - 2
count = 0
# for n in range(1,1000, 2): F(n)
# for n in range(999, 0,-1): F(n)

for n in range(1, 1000):
    if 100 <= F(n) <= 999:   count += 1
print(count)