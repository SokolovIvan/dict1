intList = list(map(int, input().split()))
intList1 = []
n = len(intList)
m = 1
while m < n:
    if intList[m] > intList[m-1]:
        intList1.append(intList[m])
    m += 1
print(*intList1)
