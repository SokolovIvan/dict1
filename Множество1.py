list1 = list(map(int, input().split()))
set1 = set()
for i in list1:
    if i in set1:
        print('YES')
    else:
        print('NO')
        set1.add(i)
