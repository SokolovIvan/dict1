intlist = list(map(int, (input().split())))
intlist1 = []
n = len(intlist)
m = 0
if n % 2 != 0:
    a = intlist[n - 1]
    intlist.pop(n - 1)
while m < n - 1:
    intlist1.append(intlist[m+1])
    intlist1.append(intlist[m])
    m += 2
if n % 2 != 0:
    intlist1.append(a)
print(*intlist1)
