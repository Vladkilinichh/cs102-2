a = input()
b = ' abcdefghijklmnopqrstuvwxyz'
res = []
len_b=len(b)
for i in a:
    res.append(b[(b.find(i)+3)%len_b]) 
print('Result: ', '"',''.join(res),'"', sep = '')
