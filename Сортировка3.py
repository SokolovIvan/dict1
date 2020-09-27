n = int(input())
L1 = list(map(int, input().split()))
m = int(input())
L2 = list(map(int, input().split()))
for i in range(n):
    L1[i] = [L1[i], i, 0]
L1.sort()
for i in range(m):
    L2[i] = [L2[i], i]
L2.sort()
j1 = 0
for i in range(n):
    mindist = L1[n - 1][0] + L2[m - 1][0]
    for j in range(j1, m):
        mindist1 = abs(L1[i][0] - L2[j][0])
        if mindist1 < mindist:
            j2 = j
            mindist = mindist1
            L1[i][2] = L2[j][1]
        else:
            break
    j1 = j2
L1.sort(key=lambda i: i[1])
for i in range(n):
    print(L1[i][2] + 1, ' ', end='')
