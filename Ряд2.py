n = int(input())
line1 = ('+___ ')
print(line1 * n)
i = 0
for i in range(0, n):
    i = i + 1
    print('|', i, ' / ', sep='', end='')
print()
line3 = ('|__\\ ')
line4 = ('|    ')
print(line3 * n)
print(line4 * n)
