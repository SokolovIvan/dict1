intList = list(map(int, input().split()))
intList1 = []
n = len(intList)
m = 0
while m < n:
    if intList[m] % 2 == 0:
        intList1.append(intList[m])
    m += 1
print(*intList1)
