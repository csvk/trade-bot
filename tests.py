d = dict(a=1, b=2)

key = 'c'

if key in d and d[key] == 1:
    print(d[key])
else:
    print(key, 'missing')