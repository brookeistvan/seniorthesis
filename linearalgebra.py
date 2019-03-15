import numpy as np
import operator as op
from functools import reduce

# let p be a vector of solutions (the real population of tweeters tweeting that number of times)
d = np.transpose(np.array([602362, 100819, 37491])) # 18441, 10577, 6708, 4612, 3331, 2259, 1709]


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

A = []
for i in range(1,4):
	a = []
	for n in range(1,21):
		if n < i:
			a.append(0)
		else:
			x = ((.1)**i)*(ncr(n,i))*((.9)**(n-i))
			a.append(x)
	A.append(a)
A = np.array(A)
print(A)
# print(np.linalg.det(A))
inverse = np.linalg.pinv(A)
print(inverse)

p = np.dot(inverse, d)
print(p)
print(sum(p))

Anew = []
for i in range(1,4):
	a = []
	for n in range(1,4):
		if n < i:
			a.append(0)
		else:
			x = ((.1)**i)*(ncr(n,i))*((.9)**(n-i))
			a.append(x)
	Anew.append(a)

pnew = [p[0], p[1], p[2]]
print(np.array(Anew).dot(np.array(pnew)))