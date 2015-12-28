import math

class BoardManager:
	boardSizeX = None
	boardSizeY = None
	p1Node = None
	p2Node = None
	next_id = -1

	#flags
	newBoardState = False
	
	#config settings
	maxDistance = -1
	distanceMetric = 'euclidean'
	numChildren = -1

	''' for best results, boardSizeX and boardSizeY should be positive integers, and configs should be a dictionary
	  __init__ will use default values if configs does not contain necessary information
	'''
	def __init__(self, boardSizeX, boardSizeY, configs = {}):
		self.boardSizeX = boardSizeX
		self.boardSizeY = boardSizeY
		
		#interpret configs dict
		self.maxDistance = configs.get('maxDistance', 25)
		self.distanceMetric = configs.get('distanceMetric', 'euclidean')
		self.numChildren = configs.get('numChildren', 3)		
		self.depth = configs.get('startDepth', 3)

		#build board
		p1Node = buildTree(1, boardSizeX / 8, boardSizeY / 2, 0, boardSizeY, self.depth, self.numChildren)
		p2Node = buildTree(2, boardSizeX - (boardSizeX / 8), boardSizeY / 2, 0, boardSizeY, self.depth, self.numChildren)
 	
	def buildTree(playerNum, x, y, ymin, ymax, depth, numChildren):
		output = Node(x, y, getNextId())

		#return a childless node if depth is 0. Else, start making the children
		if depth == 0:
			return output

		for i in range (numChildren):
			#x is current x plus half the distance between x and the center line. 
			#y is i out of (numChildren + 1) portions of the way down the part of the board allotted to this node. 
			#if you find this confusing ask Forrest about it
			dx = (abs(x - boardSizeX / 2) / 2)
			if playerNum == 2:	#if the player is on the right
				dx *= -1 
			output.addChild(buildTree(x + dx, 
									  (((float)(i * ymax))/(numChildren + 1)) + ymin, 
									  depth - 1, 
									  configs))
	''' Takes the id of the node being moved, its new x location and its new y location
	  returns True if the move was valid and False if it was invalid. 
	  if the move is valid, updates the board and sets the newBoardState flag to True
	'''
	def makeMove(pnum, id, newX, newY):
		result = False
		if pnum == 1:
			actingNode = getNode(p1Node, id)
		else:
			actingNode = getNode(p2Node, id)

		if getDistance(actingNode.x, actingNode.y, newX, newY) <= self.maxDistance:
			actingNode.x = newX
			actingNode.y = newY
			result = True

		if result == True:
			newBoardState = True

		return result

	def getNode(root, id):

		if root.getChild(id) is not None:
			return root.getChild(id)
		elif root.children is not None:
			for childID in root.children:
				output = getNode(root.getChild(childID), id)
				if output is not None:
					return output
		return None


	def getNextId():
		next_id += 1
		return next_id

	# Once we get support for different distance metrics, this function should compute the appropraite one based on distanceMetric
	def getDistance(x1, y1, x2, y2):
		return math.hypot(x2 - x1, y2 - y1)	#math.hypot(x, y) returns math.sqrt(x^2, y^2)

	def getNodeDistance(n1, n2):
		if n1 is None:
			return getDistance(0, 0, n2.x, n2.y)
		elif n2 is None:
			return getDistance(n1.x, n1.y, 0, 0)
		else:
			return getDistance(n1.x, n1.y, n2.x, n2.y)
