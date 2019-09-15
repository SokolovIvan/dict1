n = int(input())
L = []
for i in range(n):
    line1 = list(input().split())
    score = int(line1[1])
    L.append(line1)
    L[i][1] = score
    L.sort(key=lambda i: i[1], reverse=True)
for i in range(len(L)):
    print(*L[i][0], sep='')
