a = input().split()
minn = 1000
for i in range(0, len(a)):
    if int(a[i]) > 0:
        minn = min(minn, int(a[i]))
print(minn)