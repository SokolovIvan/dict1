def func(m):
    if m == 0:
        return m
    n = int(input())
    if n == 0:
        return (m)
    else:
        m = n + m
        return func(m)


m = int(input())
print(func(m))
