intList = list(map(int, input().split()))
n = len(intList)
m = 0
i = 0
a = 0
while m < n:
    if intList[m] >= i:
        i = intList[m]
        a = m
    m += 1
print(i, a)
