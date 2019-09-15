list1 = list(map(int, input().split()))
list2 = list(map(int, input().split()))
set1 = set(list1)
set2 = set(list2)
set3 = [set1 & set2]
for elem in set3:
    print(*sorted(elem, reverse=False))
