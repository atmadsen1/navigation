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

#Position data assumed to be (row,col,orientationAngle)
#figure out how much to turn based on current position data and targetNode
#when initializing, set targetNode=1
def drive (pathNodes, positionData, targetNode, closeEnough):
	#check if we are close enough to the next point
	#if yes then start referencing the next one
	dr = pathNodes[targetNode][0] - positionData[0]
	dc = pathNodes[targetNode][1] - positionData[1]
	dl = math.sqrt(dr**2 + dc**2)
	while dl < closeEnough:	#if robot is close to the target point start using the next
		targetNode += 1
		if targetNode >= len(pathNodes):
			return None	#arrived at destination
		dr = pathNodes[targetNode][0] - positionData[0]
		dc = pathNodes[targetNode][1] - positionData[1]
		dl = math.sqrt(dr**2 + dc**2)
	robotToTargetAngle = math.atan2(-dr,dc)*180/math.pi
	if (robotToTargetAngle < 0):
		robotToTargetAngle += 360
	angleDif = positionData[2]-robotToTargetAngle	#swap the subtraction for negative right turns
	if angleDif > 180:		#left
		angleDif -= 360
	elif angleDif < -180:	#right
		angleDif += 360
	#angleDif is negative if we need to turn left
	return targetNode	#not there yet, return for reuse


def nCr(n,r):	#doesn't handle error cases r<0 or r<n
	f = math.factorial
	return f(n) // f(r) // f(n-r)

if __name__=="__main__":
	path = [(2, 2), (3, 3)]
	posData = [2,2,0]
	targetNode = 1
	closeEnuf = 0.4
	test = drive(path, posData, targetNode, closeEnuf)
	print(test)

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

