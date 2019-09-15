def rec():
    n = int(input())
    if n == 0:
        print(0)
    elif n != 0:
        rec()
        if n != 0:
            print(n)
rec()
