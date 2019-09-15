intlist = list(map(int, input().split()))
n = len(intlist)
m = 0
xmax = intlist[0]
xmin = intlist[0]
while m < n:
    if intlist[m] > xmax:
        xmax = intlist[m]
    elif intlist[m] < xmin:
        xmin = intlist[m]
    m += 1
intlist1 = []
m = 0
while m < n:
    if intlist[m] != xmax and intlist[m] != xmin:
        intlist1.append(intlist[m])
    elif intlist[m] == xmax:
        intlist1.append(xmin)
    elif intlist[m] == xmin:
        intlist1.append(xmax)
    m += 1
print(*intlist1)
