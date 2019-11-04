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
			if (i < 0 or i >= 15):
				continue
			for j in range(sy, ey + 1):
				if (j < 0 or j >= 15):
					continue
				if (i == point[0] and j == point[1]):
					continue
				if (self.board[i, j] != config.empty):
					cnt -= 1
					if (cnt <= 0):
						return True
		return False

	def increment(self):
		self.counter += 1

	def decrement(self):
		self.counter -= 1

	def getCounter(self):
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
				if self.board[i][j] == config.empty:
					if self.hasNeighbor((i, j), 2, 2):
						cs = self.scorePoint((i, j), config.com)
						hs = self.scorePoint((i, j), config.hum)
						self.comScore[i, j] = cs
						self.humScore[i, j] = hs
				elif self.board[i][j] == config.com:
					self.comScore[i][j] = self.scorePoint((i, j), config.com)
					self.humScore[i][j] = 0
				else:
					self.humScore[i][j] = self.scorePoint((i, j), config.hum)
					self.comScore[i][j] = 0


	def scorePoint(self, point, role, dir = -1):
		ret = 0
		empty = 0
		cnt = block = secondCount = 0
		if dir == -1 or dir == 0:
			cnt = 1
			block = secondCount = 0
			empty = -1
			while True:
				i = point[1] + 1
				if i >= 15:
					block += 1
					break
				t = self.board[point[0], i]
				if t == config.empty:
					if empty == -1 and i < 15 - 1 and self.board[point[0], i + 1] == role:
						empty = cnt
						i += 1
						continue
					else:
						break
				if t == role:
					cnt += 1
					i += 1
					continue
				else:
					block += 1
					break

			while True:
				i = point[1] - 1
				if i < 0:
					block += 1
					break
				t = self.board[point[0], i]
				if t == config.empty:
					if empty == -1 and i > 0 and self.board[point[0], i - 1] == role:
						empty = 0
						i += 1
						continue
					else:
						break
				if t == role:
					secondCount += 1
					if empty != -1:
						empty += 1
					i += 1
					continue
				else:
					block += 1
					break
			cnt += secondCount
		ret += self.countToScore(cnt, block, empty)
		if dir == -1 or dir == 1:
			cnt = 1
			block = secondCount = 0
			empty = -1

			while True:
				i = point[0] + 1
				if i >= 15:
					block += 1
					break
				t = self.board[i, point[1]]
				if t == config.empty:
					if empty == -1 and i < 15 - 1 and self.board[i + 1, point[1]] == role:
						empty = cnt
						i += 1
						continue
					else:
						break
				if t == role:
					cnt += 1
					i += 1
					continue
				else:
					block += 1
					break
			while True:
				i = point[0] - 1
				if i < 0:
					block += 1
					break
				t = self.board[i, point[1]]
				if t == config.empty:
					if empty == -1 and i > 0 and self.board[i - 1, point[1]] == role:
						empty = 0
						i += 1
						continue
					else:
						break
				if t == role:
					secondCount += 1
					if empty != 1:
						empty += 1
					i += 1
					continue
				else:
					block += 1
					break
			cnt += secondCount

		ret += self.countToScore(cnt, block, empty)

		if dir == -1 or dir == 2:
			cnt = 1
			block = secondCount = 0
			empty = -1

			while True:
				i = 1
				x, y = point[0] + i, point[1] + i
				if x >= 15 or y >= 15:
					block += 1
					break
				t = self.board[x, y]
				if t == config.empty:
					if empty == -1 and x < 15 - 1 and y < 15 - 1 and self.board[x + 1, y + 1] == role:
						empty = cnt
						i += 1
						continue
					else:
						break
				if t == role:
					cnt += 1
					i += 1
					continue
				else:
					block += 1
					break
			while True:
				i = 1
				x, y = point[0] - i, point[1] - i
				if x < 0 or y < 0:
					block += 1
					break
				t = self.board[x, y]
				if t == config.empty:
					if empty == -1 and x > 0 and y > 0 and self.board[x - 1, y - 1] == role:
						empty = 0
						i += 1
						continue
					else:
						break
				if t == role:
					secondCount += 1
					if empty != -1:
						empty += 1
					i += 1
					continue
				else:
					block += 1
					break
			cnt += secondCount
		ret += self.countToScore(cnt, block, empty)

		if dir == -1 or dir == 3:
			cnt = 1
			block = secondCount = 0
			empty = -1

			while True:
				i = 1
				x, y = point[0] + i, point[1] - i
				if x >= 15 or y >= 15 or x < 0 or y < 0:
					block += 1
					break
				t = self.board[x, y]
				if t == config.empty:
					if empty == -1 and x < 15 - 1 and 0 < y and self.board[x + 1, y - 1] == role:
						empty = cnt
						i += 1
						continue
					else:
						break
				if t == role:
					cnt += 1
					i += 1
					continue
				else:
					block += 1
					break
			while True:
				i = 1
				x, y = point[0] - i, point[1] + i
				if x >= 15 or y >= 15 or x < 0 or y < 0:
					block += 1
					break
				t = self.board[x, y]
				if t == config.empty:
					if empty == -1 and 0 < x and y < 15 - 1 and self.board[x - 1, y + 1] == role:
						empty = 0
						i += 1
						continue
					else:
						break
				if t == role:
					secondCount += 1
					if empty != -1:
						empty += 1
					i += 1
					continue
				else:
					block += 1
					break
			cnt += secondCount

		ret += self.countToScore(cnt, block, empty)
		return ret


	def countToScore(self, cnt, block, empty):
		if empty <= 0:
			if cnt >= 5: return config.FIVE
			if block == 0:
				if cnt == 1: return config.ONE
				elif cnt == 2: return config.TWO
				elif cnt == 3: return config.THREE
				elif cnt == 4: return config.FOUR
			elif block == 1:
				if cnt == 1: return config.BLOCKED_ONE
				elif cnt == 2: return config.BLOCKED_TWO
				elif cnt == 3: return config.BLOCKED_THREE
				elif cnt == 4: return config.BLOCKED_FOUR
		elif empty == 1 or empty == cnt - 1:
			if cnt >= 6: return config.FIVE
			if block == 0:
				if cnt == 2: return config.TWO / 2
				elif cnt == 3: return config.THREE
				elif cnt == 4: return config.BLOCKED_FOUR
				elif cnt == 5: return config.FOUR
			if block == 1:
				if cnt == 2: return config.BLOCKED_TWO
				elif cnt == 3: return config.BLOCKED_THREE
				elif cnt == 4: return config.BLOCKED_FOUR
				elif cnt == 5: return config.BLOCKED_FOUR
		elif empty == 2 or empty == cnt - 2:
			if cnt >= 7: return config.FIVE
			if block == 0:
				if cnt == 3: return config.THREE
				elif cnt == 4: return config.BLOCKED_FOUR
				elif cnt == 5: return config.BLOCKED_FOUR
				elif cnt == 6: return config.FOUR
			if block == 1:
				if cnt == 3: return config.BLOCKED_THREE
				elif cnt == 4: return config.BLOCKED_FOUR
				elif cnt == 5: return config.BLOCKED_FOUR
				elif cnt == 6: return config.FOUR  # ?
			if block == 2:
				if cnt == 4 or cnt == 5 or cnt == 6: return config.BLOCKED_FOUR

