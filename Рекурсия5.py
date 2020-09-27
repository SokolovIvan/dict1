def func1(n, m):
    i = 5
    if n == 1 or m == 1:
        n = round(n)
        m = round(m)
        return n, m
    elif n % 2 == 0 and m % 2 == 0:
        n = n / 2
        m = m / 2
        return func1(n, m)
    elif n % 3 == 0 and m % 3 == 0:
        n = n / 3
        m = m / 3
        return func1(n, m)
    while i <= n and i <= m:
        if n % i == 0 and m % i == 0:
            n = n / i
            m = m / i
        else:
            i = i + 1
    if n > m and n % m == 0:
        n = n / m
        m = 1
    elif n < m and m % n == 0:
        n = 1
        m = m / n
    n = round(n)
    m = round(m)
    return n, m


def ReduceFraction(n, m):
    pq = tuple
    pq = func1(n, m)
    return pq


n, m = float(input()), float(input())
print(*ReduceFraction(n, m))
