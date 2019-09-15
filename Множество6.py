N = int(input())
dict1 = {}
dict2 = {}
for i in range(N):
    list1 = list(map(str, input().split()))
    dict1[list1[1]] = list1[0]
    dict2[list1[0]] = list1[1]
word1 = str(input())
if word1 in dict1:
    print(dict1[word1])
if word1 in dict2:
    print(dict2[word1])
