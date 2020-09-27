def is_parent(L, child):
    if L.get(child) != None:
        tmpvalue = L.get(child)
        for i in range(len(tmpvalue)):
            global tmp_set
            tmp_set.add(tmpvalue[i])
        for i in range(len(tmpvalue)):
            is_parent1(L, tmpvalue[i])

def is_parent1 (L, child):
    is_parent (L, child)

#inFile = open('input.txt', 'r', encoding='utf8')
n = int(input())
L = {}
err = set()
#for line in inFile:
#    a = list(line[0:-1:].split())
#    L[a[0]] = a[2:]
for n in range(n):
    a = str(input()).split()
    L[a[0]] = a[2::]
#print(L)
q = int(input())
for q in range(q):
    child = input()
    tmp_set = set()
    is_parent (L, child) #это мы формируем множество tmp_set
    if tmp_set.isdisjoint(err) == False:
        print(child)
    err.add(child)
