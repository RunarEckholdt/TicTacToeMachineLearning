# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 22:44:39 2020

@author: Runar
"""


 

class Board():
    def __init__(self):
        self.__board = [[],[],[]]
        for y in range(3):
            for x in range(3):
                self.__board[y].append(0)
    def printBoard(self):
        print()
        print(" x: 0  1  2")
        print("y")
        for y in range(3):
            line = str(y) + ": "
            for x in range(3):
                line += "[" + str(self.__board[y][x]) + "]"
            print(line)
    def isValidCoord(self,y,x):
        if y >= 0 and y <= 2 and x >= 0 and x <= 2:
            return True
        else:
            print("A non valid coordinate was entered")
            return False
    def pieceAtPos(self,y,x):
        if self.isValidCoord(y, x):
            return self.__board[y][x]
    
    def placePiece(self,y,x,piece):
        if self.isValidCoord(y,x):
            if self.pieceAtPos(y,x) == 0:
                self.__board[y][x] = piece
                return True
            else:
                return False
        else:
            return False
    def movePiece(self,sY,sX,y,x):
        if self.isValidCoord(sY,sX) and self.isValidCoord(y,x):
            if self.pieceAtPos(sY,sX) != 0 and self.pieceAtPos(y,x) == 0:
                self.__board[y][x] = self.__board[sY][sX]
                self.__board[sY][sX] = 0
                return True
            else:
                return False
        else:
            return False
    def getBoard(self):
        return self.__board