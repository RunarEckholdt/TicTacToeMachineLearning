import random
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np

P1 = 0
P2 = 1

class Bot():
    def __init__(self,P,model):
        self.__P = P+1
        self.__model = model
    def addFitness(self,fitnessToAdd):
        self.__fitness += fitnessToAdd
    def remFitness(self,fitnessToRem):
        self.__fitness -= fitnessToRem
    def getFitness(self):
        return self.__fitness
    def piecesLeft(self):
        return self.__piecesLeft
    # def mutateGen(self):
    #     self.__model = mutateLayers(self.gen)
    def getGen(self):
        return self.__model
    def predictChoice(self,inputData):
        return self.__model.predict([inputData])
    def getNr(self):
        return self.__player
    def remPiece(self):
        self.__piecesLeft -= 1
    def resetBot(self):
        self.__fitness = 100
        self.__piecesLeft = 3
    def resetPieces(self):
        self.__piecesLeft = 3
        

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




class Game():
    def __init__(self,b1,b2,board):
        self.__b1 = b1
        self.__b2 = b2
        self.__board = board
        self.__turnCounter = 0
        self.__finished = False
    def __getBoard(self):
        return self.__board
    def doTurn(self):
        self.__b1 = self.__takeTurn(self.__b1)
        if self.__checkForWin(self.__b1):
            self.__win(self.__b1)
        self.__b2 = self.__takeTurn(self.__b2)
        if self.__checkForWin(self.__b2):
            self.__win(self.__b2)
        self.__turnCounter += 1
    def __takeTurn(self,bot):
        if bot.piecesLeft() > 0:
            inputData = self.__getInputData(True,bot,self.__getBoard())
            
    
    
    
    def __getInputData(self,pieceChosen,player,pBoard):
        inputData = []
        for i in range(10):
            inputData.append([])
            for j in range(3):
                inputData[i].append([])
        board = pBoard.getBoard()
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    inputData[i][j] = 0
                    inputData[i+3][j] = 0
                    inputData[i+6][j] = 1
                            
                            
                elif board[i][j] == 1:
                    inputData[i][j] = 1
                    inputData[i+3][j] = 0
                    inputData[i+6][j] = 0
                
                
                elif board[i][j] == 2:
                    inputData[i][j] = 0
                    inputData[i+3][j] = 1
                    inputData[i+6][j] = 0
        if pieceChosen == True:
            inputData[9] = [1,player,0]
        else:
            inputData[9] = [0,player,0]
        return inputData
        
            
        



def readDataAsCsv():
    global yData
    global xData
    yData = []
    xData = []
    loadedData = pd.read_csv("tictactoe.csv")
    tmpyData = list(loadedData['output'].values)
    tmpxData = list(loadedData['input'].values)
    
    for i in range(len(tmpyData)):
        yData.append(int(tmpyData[i]))
    
    for i in range(len(tmpxData)):
        xData.append([])
        c = 0
        for j in range(10):
            xData[i].append([])
            valuesConverted = 0

            while valuesConverted < 3:
                try:
                    xData[i][j].append(int(tmpxData[i][c]))
                    valuesConverted += 1
                except:
                    pass
                c += 1
                
                
def createModel():
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(10,3)))
    model.add(keras.layers.Dense(30,activation='relu'))
    model.add(keras.layers.Dense(270,activation='relu'))
    model.add(keras.layers.Dense(9,activation='softmax'))
    model.compile(optimizer = "adam",loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model