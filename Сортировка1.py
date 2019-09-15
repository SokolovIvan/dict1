def merge(A, B):
    nA = len(A)
    nB = len(B)
    iA = 0
    iB = 0
    AB = []
    while iA < nA or iB < nB:
        if iB < nB and iA < nA and A[iA] < B[iB]:
            AB.append(A[iA])
            iA += 1
        elif iB < nB and iA < nA and A[iA] > B[iB]:
            AB.append(B[iB])
            iB += 1
        elif iB < nB and iA < nA and A[iA] == B[iB]:
            AB.append(B[iB])
            AB.append(A[iA])
            iB += 1
            iA += 1
        elif iB == nB and iA < nA:
            AB.append(A[iA])
            iA += 1
        elif iA == nA and iB < nB:
            AB.append(B[iB])
            iB += 1
    print(*AB)


A = list(map(int, input().split()))
B = list(map(int, input().split()))
merge(A, B)
