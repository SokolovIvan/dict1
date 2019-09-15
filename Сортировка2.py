L1 = list(map(int, input().split()))
L2 = []
for m in range(L1[1]):
    L2.append(int(input()))
S = L1[0]
N = L1[1]
L2.sort()
tv = 0
i = 0
for count in L2:
    if tv < S and i < N:
        if L2[i] < S - tv:
            tv += L2[i]
            i = i + 1
print(i)
