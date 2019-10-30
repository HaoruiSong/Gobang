import numpy as np
import config


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
        self.humScore = np.zeros((15, 15), dtype=int)
        self.comScore = np.zeros((15, 15), dtype=int)
        self.board = np.zeros((15, 15), dtype=int)
        self.zobrist = Zobrist()



class AI(Board):
    def __init__(self):
        Board.__init__(self)
        self.allsteps = []
        self.comMaxScore = 0
        self.humMaxScore = 0
        self.Max = config.FIVE
        self.Min = config.FIVE * (-1)
        self.cache = {}
        # self.count = 0
