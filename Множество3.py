inFile = open('input.txt', 'r')
outFile = open('output.txt', 'w')
n = int(inFile.readline())
set1 = set(range(1, n + 1))
i = 1
for line in inFile:
    i += 1
    a = set(line.split())
    if 'HELP' in line:
        break
    if i % 2 == 0:
        temp = set(map(int, line.split()))
    elif a == {'YES'}:
        set1 &= temp
    elif a == {'NO'}:
        set1 -= temp
print(*set1, file=outFile)
inFile.close()
outFile.close()
