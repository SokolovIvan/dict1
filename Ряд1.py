a, b = int(input()), int(input())
if a <= b:
    ab = tuple(range(a, b + 1,))
else:
    ab = tuple(range(a, b - 1, -1))
print(*ab)
