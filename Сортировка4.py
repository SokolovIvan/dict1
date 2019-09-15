inFile = open('input.txt', 'r', encoding='utf8')
outFile = open('output.txt', 'w', encoding='utf8')
L = []
for line in inFile:
    a = list(line[0:-1:].split())
    a.pop(2)
    L.append(a)
L.sort(key=lambda i: i[0])
for i in range(len(L)):
    print(*L[i], file=outFile)
inFile.close()
outFile.close()
