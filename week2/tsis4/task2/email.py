import re
n, ans = int(input()), []
for i in range(n):
    name, mail = input().split()
    if bool(re.search(r'<[a-z][\w\.\-\_]+@[a-zA-Z]+\.[a-z]{1,3}>', mail)):
        ans.append((name, mail))
for i in ans: print(*i)