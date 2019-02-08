import math

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
	return targetNode,angleDif	#not there yet, return for reuse



if __name__=="__main__":
	path = [(2, 2), (3, 3)]
	posData = [2,2,270]
	targetNode = 1
	closeEnuf = 0.4
	testNode, testAngle = drive(path, posData, targetNode, closeEnuf)
	print(testNode,testAngle)


