G = [0] * 100000
for n in range(99999, -1, -1):
    if n < 20000:
        G[n] = 20 + n + G[n + 4]
    else:
        G[n] = n * n

F = [0] * 70000
for n in range(0, 70000, 1):
    if n > 19999:
        F[n] = n + F[n - 6]
    else:
        F[n] = n + G[n - 3]

print(F[65000])
