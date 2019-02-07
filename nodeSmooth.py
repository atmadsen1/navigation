import math

#Credit to Andrew Johnson for the parametric smoothing equation
def smoothPath (rawPath,numPoints=0):
	if (numPoints == 0):
		numPoints = int(len(rawPath)/2)
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

#This needs to be inserted into the robot class that contains the location/orientation data
#This uses the smoothed path obtained from running myAlgorithm with nodeSmooth
#CODE NOT NEEDED
def anglePath (path):
	#Code to get the heading angle from one node to the next in the smoothPath nodes
	#So headingAngle[1] would be the heading angle to get from path[1] to path[2]
	headingAngles = []
	for nodeNum in range(len(path)-1):
		n1 = path[nodeNum]
		n2 = path[nodeNum+1]
		dr = n2[0] - n1[0]
		dc = n2[1] - n1[1]
		angle = math.atan2(-dr,dc)
		if (angle < 0):
			angle += 2*math.pi
		headingAngles.append(angle*180/math.pi)	#remove "*180/math.pi" to make radians
	return headingAngles

def nCr(n,r):	#doesn't handle error cases r<0 or r<n
	f = math.factorial
	return f(n) // f(r) // f(n-r)





# ________		 ___	 ___________	 ___________	 ___________
#|		  \		|	|	|			|	|			|	|			|
#|		   \	|	|	|	_____	|	|___	 ___|	|	 _______|
#|			\	|	|	|	|	|	|		|	|		|	|
#|		|\	 \	|	|	|	|	|	|		|	|		|	|_______
#|		| \	  \	|	|	|	|	|	|		|	|		|	 _______|
#|		|  \   \|	|	|	|	|	|		|	|		|	|
#|		|   \		|	|	|	|	|		|	|		|	|_______
#|		|    \		|	|	|___|	|		|	|		|			|
#|		|	  \		|	|			|		|	|		|			|
#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT

#The pathing arrays use the grid matrix system while the robot position
#utilizes real world distances. To use this code just convert the robot
#data to the matrix stuff, or the other way around.

