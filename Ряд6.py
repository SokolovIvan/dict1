intList = list(map(int, input().split()))
n = len(intList)
m = 0
i = 0
while m < n:
    if intList[m] > 0:
        i += 1
    m += 1
print(i)
