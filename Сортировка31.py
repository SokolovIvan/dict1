def func2(a, b):
    return (a - b) ** 2


def func3(a, b):   # Функция для подсчёта расстояния
    if a > b:
        return(a - b)
    elif a < b:
        return(b - a)
    elif a == b:
        return 0


def func1(village, L4, safe, safe_total):   # Функция возвращает разницу между предыдущим и текущим бомбоубежищем, для следующего селения
    mindist1 = 0   # расстояние если деревня дальше от 0 чем бомбоубежище
    mindist2 = 0   # расстояние если деревня ближе к 0 чем бомбоубежище
    j2 = 0   # количество бомбоубежищ от оптимального для прошлого селения до оптимального для текущего селения
    if village > L4[j2][1]:
        while village > L4[j2][1] and j2 + safe < safe_total - 1:   # ищем ближайшее бомбоубежище к текущему селению "снизу"
            mindist1 = func2(village, L4[j2][1])
            j2 += 1
        if village > L4[j2][1] and j2 + safe < safe_total:   # если осталось последнее бомбоубежище
            return j2
        elif village == L4[j2][1]:
            return j2
        elif village < L4[j2][1]:   # сравниваем с расстоянием до бомбоубежища сверху
            mindist2 = func2(village, L4[j2][1])
            if mindist1 < mindist2:
                return j2 - 1
            else:
                return j2
    elif village == L4[0][1]:
        return 0
    elif village < L4[j2][1]:
        return 0


n = int(input())
L1 = list(map(int, input().split()))
m = int(input())
L2 = list(map(int, input().split()))
L3 = []   # формируем список из селений, с индексом и расстояниями
for i in range(n):
    village = (int(i), L1[i])
    L3.append(village)
tuple(L3)
L4 = []   # формируем список из бомбоубежищ, с индексом и расстояниями
for i1 in range(m):
    safe = (int(i1), L2[i1])
    L4.append(safe)
tuple(L4)
L3.sort(key=lambda i: (i[1]))
L4.sort(key=lambda i: (i[1]))
j = 0
j1 = 0
L5 = []
while j < n:   # берём каждое селение из отсортированного списка, начиная с первого. и ищем подходящее для этого селения бомбоубежище.
    j3 = func1(L3[j][1], L4[j1:], j1, m)
    j1 = j1 + j3   # чтобы не перебирать заново передаём в функцию отбора последнее бомбоубежище.
    L5.append((L3[j][0], L4[j1][0] + 1))    # формируем таблицу из индексов селений, и индексов бомбоубежищ.
    j += 1
tuple(L5)
L5.sort(key=lambda i: (i[0]))
for i in range(j):
    print(L5[i][1], ' ', end='')
