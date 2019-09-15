intList = list(map(int, input().split()))
intList1 = []
n = len(intList)
m = 0
while m < n:
    if intList[m] > 0:
        intList1.append(intList[m])
    m += 1
n1 = len(intList1)
m = 1
a = intList1[0]
while m < n1:
    if intList1[m] < a:
        a = intList1[m]
    m += 1
print(a)
