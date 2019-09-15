inFile = open('input.txt', 'r', encoding='utf8')
outFile = open('output.txt', 'w', encoding='utf8')
set1 = set()
for line in inFile:
    a = list(line[0:-1].split())
    for i in a:
        set1.add(i)
print(len(set1))
