N = int(input())
set1 = set()
set3 = set()
for i in range(N):
    Mi = int(input())
    set2 = set()
    for i1 in range(Mi):
        lang = str(input())
        set2.add(lang)
    if i == 0:
        set1 = set2
    set1 &= set2
    set3 |= set2
print(len(set1))
print(*set1, sep='\n')
print(len(set3))
print(*set3, sep='\n')
