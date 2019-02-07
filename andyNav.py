import math


#This needs to be inserted into the robot class that contains the location/orientation data
#This uses the smoothed path obtained from running myAlgorithm with nodeSmooth
def navigate (smoothPath):
	#Code to get the heading angle from one node to the next in the smoothPath nodes
	headingAngles = []
	for nodeNum in range(len(smoothPath)):
		



