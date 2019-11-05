import numpy as np
import config
from functools import cmp_to_key
from point import Point
# Now I add a line directly on the website on my pc. And pull on the working copy. what will happen.

class Zobrist(object):
	def __init__(self):
		self.com = np.random.randint(low=1, high=1000000000, size=15*15)
		self.hum = np.random.randint(low=1, high=1000000000, size=15*15)
		self.code = np.random.randint(1000000000)

	def go(self, point, role):
		index = 15*point.x + point.y
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
		sx = point.x - distance
		ex = point.x + distance
		sy = point.y - distance
		ey = point.y + distance
		for i in range(sx, ex + 1):
			if (i < 0 or i >= 15):
				continue
			for j in range(sy, ey + 1):
				if (j < 0 or j >= 15):
					continue
				if (i == point.x and j == point.y):
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

	def isfive(self, point, role):
		len = 15
		cnt = 1
		i = point.y + 1
		while True:
			if i >= len: break
			t = self.board[point.x, i]
			if t != role: break
			cnt += 1
			i += 1
		i = point.y - 1
		while True:
			if i < 0: break
			t = self.board[point.x, i]
			if t != role: break
			cnt += 1
			i += 1
		if cnt >= 5: return True

		cnt = 1

		i = point.x + 1
		while True:
			if i >= len: break
			t = self.board[i, point.y]
			if t != role: break
			cnt += 1
			i += 1
		i = point.x - 1
		while True:
			if i < 0: break
			t = self.board[i, point.y]
			if t != role: break
			cnt += 1
			i += 1
		if cnt >= 5: return True

		cnt = 1

		i = 1
		while True:
			x, y = point.x + i, point.y + i
			if x >= len or y >= len: break
			t = self.board[x, y]
			if t != role: break
			cnt += 1
			i += 1
		i = 1
		while True:
			x, y = point.x - i, point.y - i
			if x < 0 or y < 0: break
			t = self.board[x, y]
			if t != role: break
			cnt += 1
			i += 1
		if cnt >= 5: return True

		cnt = 1

		i = 1
		while True:
			x, y = point.x + i, point.y - i
			if x >= len or y < 0: break
			t = self.board[x, y]
			if t != role: break
			cnt += 1
			i += 1
		i = 1
		while True:
			x, y = point.x - i, point.y + i
			if x < 0 or y >= len: break
			t = self.board[x, y]
			if t != role: break
			cnt += 1
			i += 1
		if cnt >= 5: return True
		return False

	def win(self):
		for i in range(0, 15):
			for j in range(0, 15):
				t = self.board[i, j]
				if t != config.empty:
					if self.isfive(Point(i, j), t):
						return t
		return -1

	def initScore(self):
		for i in range(0, 15):
			for j in range(0, 15):
				if self.board[i][j] == config.empty:
					if self.hasNeighbor(Point(i, j), 2, 2):
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

#  point[x, y, score, step]
	def scorePoint(self, point, role, dir=-1):
		ret = 0
		empty = 0
		cnt = block = secondCount = 0
		if dir == -1 or dir == 0:
			cnt = 1
			block = secondCount = 0
			empty = -1
			i = point.y + 1
			while True:

				if i >= 15:
					block += 1
					break
				t = self.board[point.x, i]
				if t == config.empty:
					if empty == -1 and i < 15 - 1 and self.board[point.x, i + 1] == role:
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
			i = point.y - 1
			while True:

				if i < 0:
					block += 1
					break
				t = self.board[point.x, i]
				if t == config.empty:
					if empty == -1 and i > 0 and self.board[point.x, i - 1] == role:
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
			i = point.x + 1
			while True:

				if i >= 15:
					block += 1
					break
				t = self.board[i, point.y]
				if t == config.empty:
					if empty == -1 and i < 15 - 1 and self.board[i + 1, point.y] == role:
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
			i = point.x - 1

			while True:

				if i < 0:
					block += 1
					break
				t = self.board[i, point.y]
				if t == config.empty:
					if empty == -1 and i > 0 and self.board[i - 1, point.y] == role:
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
			i = 1
			while True:

				x, y = point.x + i, point.y + i
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
			i = 1
			while True:

				x, y = point.x - i, point.y - i
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
			i = 1
			while True:

				x, y = point.x + i, point.y - i
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
			i = 1
			while True:

				x, y = point.x - i, point.y + i
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
			elif block == 1:
				if cnt == 3: return config.BLOCKED_THREE
				elif cnt == 4: return config.BLOCKED_FOUR
				elif cnt == 5: return config.BLOCKED_FOUR
				elif cnt == 6: return config.FOUR  # ?
			elif block == 2:
				if cnt == 4 or cnt == 5 or cnt == 6: return config.BLOCKED_FOUR
		elif empty == 3 or empty == cnt - 3:
			if cnt >= 8: return config.FIVE
			if block == 0:
				if cnt == 4 or cnt == 5: return config.THREE
				elif cnt == 6: return config.BLOCKED_FOUR
				elif cnt == 7: return config.FOUR
			elif block == 1:
				if cnt == 4 or cnt == 5 or cnt == 6: return config.BLOCKED_FOUR
				elif cnt == 7: return config.FOUR
			elif block == 2:
				if 4 <= cnt <= 7: return config.BLOCKED_FOUR
		elif empty == 4 or empty == cnt - 4:
			if cnt >= 9: return config.FIVE
			if block == 0:
				if 5 <= cnt <= 8:return config.FOUR
			elif block == 1:
				if 4 <= cnt <= 7: return config.BLOCKED_FOUR
				elif cnt == 8: return  config.FOUR
			elif block == 2:
				if 5 <= cnt <= 8: return config.BLOCKED_FOUR
		elif empty == 5 or empty == cnt - 5: return config.FIVE

		return 0

	def pointCompare(self, a, b):
		if a.score == b.score:
			if a.score >= 0:
				if a.step != b.step: return a.step < b.step
				else: return b.step < a.step
			else:
				if a.step != b.step: return a.step > b.step
				else: return b.step > a.step
		else: return b.score < a.score

	def deeping(self, deep):
		candidates = self.gen(config.com)
		Cache = {}
		for i in range(2, deep + 1, 2):
			bestScore = self.negamax(candidates, i, -1 * config.FIVE, config.FIVE)
			if bestScore >= config.FIVE: break

		candidates = sorted(candidates, cmp_to_key(self.pointCompare))
		result = candidates[0]
		return result



	def gen(self, role, onlyThrees=False, starSpread=False):
		fives = []
		comfours = []
		humfours = []
		comblockedfours = []
		humblockedfours = []
		comtwothrees = []
		humtwothrees = []
		comthrees = []
		humthrees = []
		comtwos = []
		humtwos = []
		neighbors = []
		si = sj = 0
		ei = ej = 14
		lastpoint1, lastpoint2 = Point(), Point # point len = 4

		if starSpread:
			i = len(self.allsteps) - 1
			while lastpoint1.x != -1 and i >= 0:
				p = self.allsteps[i]
				if p.role != role and p.attack != role:
					lastpoint1 = p
				i -= 2

			if lastpoint1.x != -1:
				lastpoint1 = self.allsteps[0] if self.allsteps[0].role != role else self.allsteps[1]

			i = len(self.allsteps) - 2
			while lastpoint2.x != -1 and i >= 0:
				p = self.allsteps[i]
				if p.attack == role:
					lastpoint2 = p
				i -= 2

			if lastpoint2.x != -1:
				lastpoint2 = self.allsteps[0] if self.allsteps[0].role != role else self.allsteps[1]

			si = min(lastpoint1.x - 5, lastpoint2.x - 5)
			sj = min(lastpoint1.y - 5, lastpoint2.y - 5)
			si = max(si, 0)
			sj = max(sj, 0)
			ei = max(lastpoint1.x + 5, lastpoint2.x + 5)
			ej = max(lastpoint1.y + 5, lastpoint2.y + 5)
			ei = min(14, ei)
			ej = min(14, ej)

		for i in range(si, ei + 1):
			for j in range(sj, ej + 1):
				if self.board[i, j] == config.empty:
					if len(self.allsteps) < 6:
						if not self.hasNeighbor(Point(i, j), 1, 1): continue
					elif not self.hasNeighbor(Point(i, j), 2, 2): continue
					p = Point(i, j)
					# TODO finish the defination of this function


	def negamax(self, candidates, deep, alpha, beta):
		pass


