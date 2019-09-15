def sum(a, b):
    if b != 0:
        sum(a + 1, b - 1)
    else:
        print(a)
        return a
a = int(input())
b = int(input())
sum(a, b)
