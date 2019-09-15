inFile = open('input.txt', 'r')
outFile = open('output.txt', 'w')
n = str(inFile.read())
list1 = n.split()
dict1 = {}
for i in list1:
    dict1[i] = dict1.get(i, -1) + 1
    print(dict1[i], ' ', end='')
