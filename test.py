import random
l=[]
with open('./animal.txt',encoding='UTF8') as f:
    for line in f:
        if line!='\n':
            l.append(line)
list(map(lambda x:x.strip(),l))[random.randint(0,70)]

a=[1,2]
print(random.sample(a,1))