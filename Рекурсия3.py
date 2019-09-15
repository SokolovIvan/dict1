def powerquick(a, n):
    if n == 0:
        return 1
    elif n % 2 == 0:
        return (powerquick(a ** 2, n / 2))
    elif n % 2 != 0:
        return a * powerquick(a, n - 1)


a = float(input())
n = int(input())
print(powerquick(a, n))
