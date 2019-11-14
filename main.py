from board import Board
from board import Zobrist
from board import AI
from game import Game
import config



if __name__ == '__main__':
    g = Game()
    while True:
        x = int(input("please input the x position of the chessman: "))
        y = int(input("please input the y position of the chessman: "))
        g.set(x, y, config.hum)
        temp = g.check()
        if temp == 1:
            print("computer wins!")
            break
        elif temp == 2:
            print("human wins!")
            break
        comPoint = g.begin()
        print("computer put the chessman on the position: ", comPoint.x, comPoint.y)
        temp = g.check()
        if temp == 1:
            print("computer wins!")
            break
        elif temp == 2:
            print("human wins!")
            break
        for i in g.board.allsteps:
            print(i.x, i.y, i.role)

        # print(g.board.board)


