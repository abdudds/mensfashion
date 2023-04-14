a = [1,2,3,3,4,4,5,5,8,5]
l = len(a)
b = []
for i in a:
    for j in range(l):
        if j!=a.index(i):
            if i == a[j]:
                b.append(i)
print(set(b))