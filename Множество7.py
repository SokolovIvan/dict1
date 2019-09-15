def mysort(list2, min1):
    if list2[0][0] > min1:
        list4.clear()
        i = 0
        list4.append(list2[i])
        while list2[i][0] == list2[i + 1][0]:
            list4.append(list2[i + 1])
            i += 1
        list4.sort()
        return(list4)
    else:
        list4.clear()
        list2.sort()
        return(list2)


inFile = open('input.txt', 'r', encoding='utf8')
list1 = inFile.read().split()
dict1 = {}
list2 = []
list3 = ()
list4 = []
list5 = []
for i in list1:
    dict1[i] = dict1.get(i, 0) + 1
print(dict1)
min1 = min(dict1.values())
list2 = [(key1, value1) for value1, key1 in dict1.items()]
list2.sort(reverse=True)
print(list2[0][0])
while len(list2) > 0:
    list4 = mysort(list2, min1)
    list6 = list4.copy()
    list5.extend(list6)
    for i in range(len(list4)):
        list2.pop(0)
for i in range(len(list5)):
    print(list5[i][1])
