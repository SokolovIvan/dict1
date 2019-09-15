def func1(n2):  #считаем минимальный делитель. Правилен именно вариант c делением на само себя.
    i = 2
    if n2 == 1:
        print('На вход подана 1, получаем 1')
        return n2
    elif n2 % i == 0:
        print('Чётное значение, делитель берём 2', 2)
        n2 = 2
        return n2
    i = 3
    while n2 % i != 0:
        i += 2
        if i > n2 ** 0.5:
            print ('Делителя нет берём само число', n2)
            return n2
    print ('Нашли иной делитель, или 3', i)
    return (i)

def func2(n2): # остаток от деления вообще не понимаю зачем эту функцию писал
   n3 = func1(n2)
   print('n3', n3)
   if n3 != n2:
       print('n2', n2)
       func2(n2 / func1(n2))
   return n3

def func3(n, m): # если и пока минимальный делитель совпадает
    print('Делители n m', func1(n), func1(m), n, m)
    if func1(n) != func1(m):
        print('Конец функции', n, m)
        return n, m
    else:
        print('Новые значения', n, m)
        return func3(n / func1(n), m / func1(m))

def func4(n, m):
    if func1(n) > func1(m):
        n = n
        m = m /func1(m)
        print ('N больше M делим М')
        return func4(n, m)
    elif func1(n) < func1(m):
        n = n / func1(n)
        m = m
        print('M больше N делим N')
        return func4(n, m)
    elif func1(n) == func1(m):
        print('Делители совпали', m, n)
        return (n, m)
    elif n == func1(n):
        print('N дошла до конца')
        return (n)
    elif m == func1(m):
        print('M дошла до конца')
        return (m)

n, m = int(input()), int(input())
func3(n, m)






print('Ответы', func3(n, m))

#print(func3(n, m))
#n2 = int(input())
#print('Ответ', func2(n2))
