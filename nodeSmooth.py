import math

def smoothPath (rawPath,numPoints=50):
	betterPath = []
	n = len(rawPath)-1
	for tint in range(numPoints+1):	# 0 to 1
		Brow = 0
		Bcol = 0
		t = tint/numPoints
		a = 1-t
		for i in range(n+1):	#summation
			base = nCr(n,i) * (a**(n-i)) * (t**i)
			Brow += base * rawPath[i][0]
			Bcol += base * rawPath[i][1]
		betterPath.append((Brow,Bcol))
	return betterPath

def nCr(n,r):	#doesn't handle error cases r<0 or r<n
	f = math.factorial
	return f(n) // f(r) // f(n-r)



