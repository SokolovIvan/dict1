def func1(n):
    if n != 0:
        n = n - 1
        func1(n)
        if n != 0:
            i = 0
            for i in range(0, n):
                i = i + 1
                print(i, sep='', end='',)
            print()


n = int(input())
func1(n+1)
