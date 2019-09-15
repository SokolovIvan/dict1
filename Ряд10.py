b = int(input())
mylist = list(map(int, (input().split())))
x = int(input())
n = len(mylist)
m = 1
a = (mylist[0] - x) ** 2
x1 = mylist[0]
while m < n:
    if (mylist[m] - x) ** 2 < a:
        a = (mylist[m] - x) ** 2
        x1 = mylist[m]
    m += 1
print(x1)
