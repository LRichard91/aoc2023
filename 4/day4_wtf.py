m = [len(set(l[:40].split()) & set(l[42:].split())) for l in open('input.txt')]
c = [1] * len(m)
for i, n in enumerate(m):
    for j in range(n): c[i + j + 1] += c[i]
print(sum(2 ** (n - 1) for n in m if n > 0), sum(c))
