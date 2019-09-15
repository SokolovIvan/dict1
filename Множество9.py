inFile = open('input.txt', 'r', encoding='utf8')
outFile = open('output.txt', 'w', encoding='utf8')
data1 = inFile.read().splitlines()
dict1 = {}
j = len(data1)
for i in data1:
    dict1[i] = dict1.get(i, 0) + 1
dict1 = [(value1, key1) for key1, value1 in dict1.items()]
dict1.sort(reverse=True)
if dict1[0][0] > j * 0.5:
    print(dict1[0][1], file=outFile)
else:
    print(dict1[0][1], '\n', dict1[1][1], sep='', file=outFile)
