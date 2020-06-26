# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:49:58 2020

@author: Runar
"""

import random
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np

csvFileExists = True
botsPlay = True

class Board():
    def __init__(self):
        self.board = [[],[],[]]
        for y in range(3):
            for x in range(3):
                self.board[y].append(0)
    def printBoard(self):
        print()
        print(" x: 0  1  2")
        print("y")
        for y in range(3):
            line = str(y) + ": "
            for x in range(3):
                line += "[" + str(self.board[y][x]) + "]"
            print(line)
    def isValidCoord(self,y,x):
        if y >= 0 and y <= 2 and x >= 0 and x <= 2:
            return True
        else:
            print("A non valid coordinate was entered")
            return False
    def pieceAtPos(self,y,x):
        if self.isValidCoord(y, x):
            return self.board[y][x]
    
    def placePiece(self,y,x,piece):
        if self.isValidCoord(y,x):
            if self.pieceAtPos(y,x) == 0:
                self.board[y][x] = piece
                return True
            else:
                return False
        else:
            return False
    def movePiece(self,sY,sX,y,x):
        if self.isValidCoord(sY,sX) and self.isValidCoord(y,x):
            if self.pieceAtPos(sY,sX) != 0 and self.pieceAtPos(y,x) == 0:
                self.board[y][x] = self.board[sY][sX]
                self.board[sY][sX] = 0
                return True
            else:
                return False
        else:
            return False
    def getBoard(self):
        return self.board
    def resetBoard(self):
        for y in range(3):
            for x in range(3):
                self.board[y][x] = 0
            
class Bot():
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.fitness = 100
    def addData(self,_input,output):
        self.inputs.append(_input)
        self.outputs.append(output)
    def addFitness(self,fitnessToAdd):
        self.fitness += fitnessToAdd
    def remFitness(self,fitnessToRem):
        self.fitness -= fitnessToRem
    def getFitness(self):
        return self.fitness
   
class Player():
    def __init__(self,shape):
        self.piecesInHand = 3
        self.shape = shape
    def placePiece(self):
        self.piecesInHand -= 1
    def piecesLeft(self):
        return self.piecesInHand
    def getShape(self):
        return self.shape



playBoard = Board()

xData = []
yData = []

if csvFileExists:
    loadedData = pd.read_csv("tictactoe.csv")
    tmpyData = list(loadedData['output'].values)
    tmpxData = list(loadedData['input'].values)
    
    for i in range(len(tmpyData)):
        yData.append(int(tmpyData[i]))
    
    for i in range(len(tmpxData)):
        xData.append([])
        for j in range(4):
            xData[i].append([])
            valuesConverted = 0
            c = 0
            while valuesConverted < 3:
                try:
                    xData[i][j].append(int(tmpxData[i][c]))
                    valuesConverted += 1
                except:
                    pass
                c += 1
                   
    
    
    
    # print(yData)
    # print(xData)


players = []
players.append(Player(1))
players.append(Player(2))
inputDataP1 = []
outputDataP1 = []
inputDataP2 = []
outputDataP2 = []


model = keras.Sequential()
model.add(keras.layers.Flatten(input_shape=(4,3)))
model.add(keras.layers.Dense(12,activation='relu'))
model.add(keras.layers.Dense(9,activation='softmax'))

model.compile(optimizer = "adam",loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(xData,yData, epochs=100)



def createModel():
    global model
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(4,3)))
    model.add(keras.layers.Dense(12,activation='relu'))
    model.add(keras.layers.Dense(9,activation='softmax'))
    model.compile(optimizer = "adam",loss="sparse_categorical_crossentropy", metrics=["accuracy"])


def translateOD(y,x):
    dta = [
        [0,1,2],
        [3,4,5],
        [6,7,8]]
    
    return dta[y][x]
   
def translateOD2(number):
    dta = [[0,0],[0,1],[0,2],
           [1,0],[1,1],[1,2],
           [2,0],[2,1],[2,2]]
    
    return dta[number]

def addDataToP1(y,x,pieceChosen,board):
    b = []
    for i in range(len(board)):
        b.append(board[i].copy())
    b.append([pieceChosen,1,0])
    inputDataP1.append(b)
    outputDataP1.append(translateOD(y,x))

def addDataToP2(y,x,pieceChosen,board):
    b = []
    for i in range(len(board)):
        b.append(board[i].copy())
    b.append([pieceChosen,2,0])
    inputDataP2.append(b)
    outputDataP2.append(translateOD(y,x))


def getIndex(value,_list):
    for i in range(len(_list)):
        if _list[i] == value:
            return i
    

def placePiece(player):
    while(True):
        board = playBoard.getBoard()
        inputData = []
        inputData.append([])
        for i in range(len(board)):
            inputData[0].append(board[i].copy())
        inputData[0].append([1,player+1,0])
        if botsPlay:
            prediction = model.predict(inputData)
            predictionSorted = np.sort(prediction[0])
            
            
            n = len(prediction[0])-1
            index = 0
            while(n>0):
                index = getIndex(predictionSorted[n],prediction[0])
                cords = translateOD2(index)
                y = cords[0]
                x = cords[1]
                if playBoard.pieceAtPos(y,x) == 0:
                    break
                else:
                    n -= 1
            # cords = np.argmax(prediction[0])
            # cords = translateOD2(cords)
            
            print("Y:", y, "X:",x)
        else:
            print("Location to place piece")
            y = int(input("Y: "))
            x = int(input("X: "))
        
        
        if playBoard.placePiece(y,x,players[player].getShape()):
            players[player].placePiece()
            if player == 0:
                addDataToP1(y,x,1,board)
            else:
                addDataToP2(y,x,1,board)
            break
        else:
            print("Invalid location")

def movePiece(player):
    while(True):
        board = playBoard.getBoard()
        inputData = []
        inputData.append([])
        if botsPlay:
            for i in range(len(board)):
                inputData[0].append(board[i].copy())
            inputData[0].append([0,player+1,0])
            prediction = model.predict(inputData)
            predictionSorted = np.sort(prediction[0])
            n = len(prediction[0])-1
            index = 0
            while(n>0):
                index = getIndex(predictionSorted[n],prediction[0])
                cords = translateOD2(index)
                sY = cords[0]
                sX = cords[1]
                if playBoard.pieceAtPos(sY,sX) == player+1:
                    break
                else:
                    n -= 1
            inputData[0][3] = [1,player+1,0]
            prediction = model.predict(inputData)
            predictionSorted = np.sort(prediction[0])
            n = len(prediction[0])-1
            index = 0
            while(n>0):
                index = getIndex(predictionSorted[n],prediction[0])
                cords = translateOD2(index)
                y = cords[0]
                x = cords[1]
                if playBoard.pieceAtPos(y,x) == 0:
                    break
                else:
                    n -= 1
        else:
            print("Location of piece to move")
            sY = int(input("Y: "))
            sX = int(input("X: "))
            if playBoard.pieceAtPos(sY, sX) == players[player].getShape():
                print("Location to place piece")
                y = int(input("Y: "))
                x = int(input("X: "))
            
            
        if playBoard.movePiece(sY,sX,y,x):
            if player == 0:
                addDataToP1(sY,sX,0,board)
                addDataToP1(y,x,1,board)
            else:
                addDataToP2(sY, sX, 0,board)
                addDataToP2(y,x,1,board)
            break
        else:
            print("Invalid Piece")

def checkForWin(player):
    board = playBoard.getBoard()
    shape = players[player].getShape()
    for y in range(2):
        if board[y] == [shape,shape,shape]:
            return True
    for x in range(2):
        if board[0][x] == board[1][x] and board[2][x] == board[0][x] and board[0][x] == shape:
            return True
    if board[1][1] == shape:
        if board[0][0] == shape and board[2][2] == shape:
            return True
        if board[0][2] == shape and board[2][0] == shape:
            return True
    return False
            

def doTurn(player):
    if players[player].piecesLeft() > 0:
        placePiece(player)
        
    else:
        movePiece(player)
    if checkForWin(player):
        return True
    else:
        return False

def win(player):
    if player == 0:
        print("P1 won")
        for i in range(len(inputDataP1)):
            print(i)
            print(inputDataP1[i])
            xData.append(inputDataP1[i])
            yData.append(outputDataP1[i])
    else:
         print("P2 won")
         for i in range(len(inputDataP2)):
             xData.append(inputDataP2[i])
             yData.append(outputDataP2[i])
        
    

def game():
    while(True):
        playBoard.printBoard()
        if doTurn(0):
            win(0)
            break
        playBoard.printBoard()
        if doTurn(1):
            win(1)
            break  
def resetGameValues():
    global playBoard
    playBoard = Board()
    players.clear()
    inputDataP1.clear()
    outputDataP1.clear()
    inputDataP2.clear()
    outputDataP2.clear()
    players.append(Player(0))
    players.append(Player(1))
    

def writeDataToFile():
    if xData[0] != "input":
        xData.insert(0,"input")
        yData.insert(0,"output")
    dataset = pd.Series(xData,yData)
    dataset.to_csv("tictactoe.csv")

def main():
    while(True):
        game()
        #ans = input("play again? (y/n)")
        #if ans == "n":
        break
        #else:
         #   resetGameValues()
    writeDataToFile()
    
    
    
main()
# playBoard.placePiece(0,0,1)
# playBoard.printBoard()
# playBoard.movePiece(0,0,0,1)

# playBoard.printBoard()



