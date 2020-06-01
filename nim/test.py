# d ={(1,2):'maciek',(1,3):'mama'}
#
# q =[(1,3),(1,4),(2,4),(1,9)]
# #
# # for i in d:
# #     print(list(i)[0])
#
from numpy.random import choice
from numpy.random import uniform
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#
# # print(a)
# if type(a) is tuple:
#     print(a)
# else:
#     print(a[round(uniform(0,len(a)-1))])
# # if len(a) == 1:
# #     print(a)
# # else:
# #     print(choice(a))
# a,b = (1,2)
# print(a)
# print(bool(d.get((1,2))))
#
# c = dict()
# c[(1,2)]= 'k'
# print(c.get(([1,2],(1,2))))


a = {(repr([1,2]),(1,2)):1,(repr([1,3]),(1,3)):3}
df = pd.DataFrame(data=list(a.values()),index=a.keys(),columns=['Score'])

# plt.plot(list(df['Score'].keys()),list(df['Score']))
# plt.show()

# print(list(df['Score'].keys()))
# print(list(list(df['Score'].keys())[0])[1])
# plt.plot([1,2,3,4,5],[4,6,7,8,9])
# plt.hist(range(0,len(list(df['Score']))),list(df['Score']))
X = plt.figure(figsize=(10,6))
for i in range(0,len(list(df['Score']))):
    plt.bar(i, height=list(df['Score'])[i])
plt.legend(list(df['Score'].keys()))
# plt.imshow(X)
plt.show(block=False)
plt.pause(3)  # 3 seconds, I use 1 usually
plt.close("all")