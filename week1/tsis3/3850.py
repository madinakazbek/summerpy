a = input().split()
n = len(a)
zero = a.count('0')
for i in range(0, len(a)):
    if a[i] != '0':
        print(a[i], end=' ')
for i in range(0, zero):
    print(0, end=' ')
