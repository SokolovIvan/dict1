B = int(input())
A = list(map(int, input().split()))
A.sort()
print(' '.join(map(str, A)))
