def CountSort(A):
    num1 = [0] * 101
    for i in A:
        num1[i] += 1
    for i in range(101):
        print((str(i) + ' ') * num1[i], end='')


A = list(map(int, input().split()))
CountSort(A)
