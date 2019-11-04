import numpy as np
import config
# Now I add a line directly on the website on my pc. And pull on the working copy. what will happen.

class Zobrist(object):
    def __init__(self):
        self.com = np.random.randint(low=1, high=1000000000, size=15*15)
        self.hum = np.random.randint(low=1, high=1000000000, size=15*15)
        self.code = np.random.randint(1000000000)

    def go(self, point, role):
        index = 15*point[0] + point[1]
        if role == config.com:
            self.code ^= self.com[index]
        else:
            self.code ^= self.hum[index]
        return self.code


class Board(object):
    def __init__(self):
        self.counter = 0  # number of chessmen
        self.board = np.zeros((15, 15), dtype=int)
        self.zobrist = Zobrist()
        
    def hasNeighbor(self, point, distance, cnt):
    	sx = point[0] - distance
    	ex = point[0] + distance
    	sy = point[1] - distance
    	ey = point[1] + distance
    	for i in range(sx, ex + 1):
    		if (i < 0 || i >= 15):
    			continue
    		for j in range(sy, ey + 1):
    			if (j < 0 || j >= 15):
    				continue
    			if (i == point[0] && j == point[1]):
    				continue
    			if (self.board[i, j] != config.empty):
    				cnt -= 1
    				if (cnt <= 0):
    					return True
    	return False
    
    def increment():
    	self.counter += 1
    
    def decrement():
    	self.counter -= 1
    
    def getCounter():
    	return self.counter
    
    



class AI(Board):
    def __init__(self):
        Board.__init__(self)
        self.humScore = np.zeros((15, 15), dtype=int)
        self.comScore = np.zeros((15, 15), dtype=int)
        self.allsteps = []
        self.comMaxScore = 0
        self.humMaxScore = 0
        self.Max = config.FIVE
        self.Min = config.FIVE * (-1)
        self.cache = {}
        # self.count = 0
        self.initScore()
        
    
    def initScore(self):
    	for i in range(0, 15):
    		for j in range(0, 15):
    			if (self.board[i][j] == config.empty):
    				if (self.hasNeighbor((i, j), 2, 2):
    					cs = self.scorePoint((i, j), config.com)
    					hs = self.scorePoint((i, j), config.hum)
    					self.comScore[i, j] = cs
    					self.humScore[i, j] = hs
    			else if (self.board[i][j] == config.com):
    				self.comScore[i][j] = scorePoint((i, j), config.com)
    				self.humScore[i][j] = 0
    			else:
    				self.humScore[i][j] = scorePoint((i, j), config.hum)
    				self.comScore[i][j] = 0
    				

