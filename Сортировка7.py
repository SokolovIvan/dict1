def func1(L, shft):
    while L[shft][0] == L[shft + 1][0]:
        shft += 1
    return shft + 1


inFile = open('input.txt', 'r', encoding='utf8')
outFile = open('output.txt', 'w', encoding='utf8')
L = []
for line in inFile:
    a = list(line[0:-1:].split())
    if len(a) < 4:
        vacan = int(a[0])
    else:
        a = list(line[0:-1:].split())
        b = a[-3:]
        score1 = int(b[0])
        score2 = int(b[1])
        score3 = int(b[2])
        scoreTotal = score1 + score2 + score3
        line1 = [scoreTotal, score1,  score2, score3]
        L.append(line1)
for i in range(len(L)):
    if L[i][1] < 40 or L[i][2] < 40 or L[i][3] < 40:
        L[i][0] = -1
L.append([-1])
L.sort(key=lambda i: i[0], reverse=True)
student = 0
shft = 0
while shft < len(L) and L[shft][0] > 119 and vacan >= student:
    student = func1(L, shft)
    if student <= vacan:
        shft = student
answ = L[shft - 1][0]
if answ == -1:
    print(1, file=outFile)
elif answ == 120:
    print(0, file=outFile)
elif L[shft][0] == -1:
    print(0, file=outFile)
else:
    print(answ, file=outFile)
inFile.close()
outFile.close()
