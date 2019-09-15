inFile = open('input.txt', 'r')
letS = inFile.read().split()
myLets = {}
for let in letS:
    myLets[let] = myLets.get(let, 0) + 1
myLets = [(fr, lt) for lt, fr in myLets.items()]


def makeSort(lws):
    return (-lws[0], lws[1])



myLets.sort(key=makeSort)
for i in range(len(myLets)):
    print(myLets[i][1])

