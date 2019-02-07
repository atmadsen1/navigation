
 
class AStarGraph(object):
 
	def __init__(self,obstacles,width,height):
		self.obstacles = obstacles
		self.width = width
		self.height = height
 
	def heuristic(self, start, goal):
		#Use Euclidean distance heuristic if we can move one square either
		#adjacent or diagonal
		D = 1 	#horizontal/vertical distance
		dr = abs(start[0] - goal[0])
		dc = abs(start[1] - goal[1])
		return D * abs(dc-dr) + 1.414 * min(dr,dc) #1.414~sqrt(2)
 		
	def get_vertex_neighbours(self, pos):
		n = []
		#Moves allow link a chess king
		for dr, dc in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
			r2 = pos[0] + dr
			c2 = pos[1] + dc
			if (c2 < 0 or c2 > self.width or r2 < 0 or r2 > self.height):	#if move is in-bounds
				continue
			n.append((r2, c2))
		return n
 
	def move_cost(self, prev, cur, to):
		if self.obstacles.count(to):
			return 1000 #Extremely high cost to enter obstacles
		rowDif = (cur[0]!=to[0]) and (cur[0]!=prev[0]) and (to[0]!=prev[0])
		colDif = (cur[1]!=to[1]) and (cur[1]!=prev[1]) and (to[1]!=prev[1])
		rowSame = (prev[0]==cur[0] and cur[0]==to[0])
		colSame = (prev[1]==cur[1] and cur[1]==to[1])

		if (rowDif and colDif):
			return 1.414	#straight diagonal
		elif (rowSame and colDif) or (colSame and rowDif):
			return 1 		#straight horizontal/vertical
		elif ((prev[0]!=cur[0] and prev[1]!=cur[1]) or (to[0]!=cur[0] and to[1]!=cur[1])) and (prev[0]!=to[0] and prev[1]!=to[1]):
			return 5 		#soft turn
		return 20 			#none of the above
 
def AStarSearch(navPoints, behind, graph):
	start = tuple(navPoints[0])
	end =   tuple(navPoints[1])

	G = {} #Actual movement cost to each position from the start position
	F = {} #Estimated movement cost of start to end going via this position
 
	#Initialize starting values
	G[start] = 0 
	F[start] = graph.heuristic(start, end)
 
	closedVertices = set()
	openVertices = set([start])
	cameFrom = {}
	prev = None

	while len(openVertices) > 0:
		#Get the vertex in the open list with the lowest F score
		current = None
		currentFscore = None
		for pos in openVertices:
			if current is None or F[pos] < currentFscore:
				currentFscore = F[pos]
				current = pos
		if (prev is None):
			prev = behind	#SET TO POSITION BEHIND ROBOT
		else:
			prev = cameFrom[current]
 
		#Check if we have reached the goal
		if current == end:
			#Retrace our route backward
			path = [current]
			while current in cameFrom:
				current = cameFrom[current]
				path.append(current)
			path.reverse()
			return path, F[end] #Done!
 
		#Mark the current vertex as closed
		openVertices.remove(current)
		closedVertices.add(current)
 
		#Update scores for vertices near the current position
		for neighbour in graph.get_vertex_neighbours(current):
			if neighbour in closedVertices: 
				continue #We have already processed this node exhaustively
			candidateG = G[current] + graph.move_cost(prev, current, neighbour)
 
			if neighbour not in openVertices:
				openVertices.add(neighbour) #Discovered a new vertex
			elif candidateG >= G[neighbour]:
				continue #This G score is worse than previously found
 
			#Adopt this G score

			cameFrom[neighbour] = current
			G[neighbour] = candidateG
			H = graph.heuristic(neighbour, end)
			F[neighbour] = G[neighbour] + H

