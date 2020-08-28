import random
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np

P1 = 0
P2 = 1
doPrintBoard = False

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
        prediction = self.__model.predict([inputData])
        return prediction[0]
    def getShape(self):
        return self.__P
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
        if self.__checkForWin(self.__b1.getShape()):
            self.__win(P1)
        self.__b2 = self.__takeTurn(self.__b2)
        if self.__checkForWin(self.__b2.getShape()):
            self.__win(P2)
        self.__turnCounter += 1
        self.__b1.remFitness(1)
        self.__b2.remFitness(1)
    def __terminateGame(self):
        self.__finished = True
    def __takeTurn(self,bot):
        #if bot must choose a piece
        if bot.piecesLeft() == 0:
            inputData1 = self.__getInputData(False,bot.getShape())
            prediction = bot.predictChoice(inputData1)
            predictionSorted = np.sort(copy2DList(prediction)) #kopierer prediction og sorterer listen
            bot, y1, x1 = self.__getValidPrediction(bot, prediction, predictionSorted, False)
        inputData2 = self.__getInputData(True,bot.getShape())
        prediction = bot.predictChoice(inputData2)
        predictionSorted = np.sort(copy2DList(prediction))
        bot,y2,x2 = self.__getValidPrediction(bot, prediction, predictionSorted, True)
        try:
            if bot.piecesLeft() == 0:
                self.getBoard().movePiece(y1,x1,y2,x2)
            else:
                bot.remPiece()
                self.getBoard().placePiece(y2,x2,bot.getShape())
        except:
            print("Bot has failed to move, game is terminated")
            bot.remFitness(100)
            self.__terminateGame()
        return bot
            
    def __getValidPrediction(self,bot,prediction,predictionSorted,pieceChosen):
        n = len(prediction[0])-1
        predIndex = 0
        shape = bot.getShape()
        board = self.__getBoard()
        while(n>0):
            predIndex = getIndex(predictionSorted[n],prediction[0])
            y,x = self.__translateOTC(predIndex)
            
            #hvis den velger sin egen brikke og ingen brikke er valgt
            if board.pieceAtPos(y,x) == shape and pieceChosen == False:
                break
            #hvis den har valgt en brukke og plassen er tom
            elif board.pieceAtPos(y,x) == 0 and pieceChosen == True:
                break
            #den faila en predict
            else:
                n -= 1
                bot.remFitness(20)
        return bot, y, x
    
    
    def __getInputData(self,pieceChosen,shape):
        inputData = []
        for i in range(10):
            inputData.append([])
            for j in range(3):
                inputData[i].append([])
        board = self.__getBoard()
        #go throu every location on the board, put 1 in every "pieces" assigned board
        #the first 3 arrays is allocated to P1, next 3 to P2, next 3 to empty board
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
        #the 10: first bit is high if piece is chosen, second bit is high if P2
        if pieceChosen == True:
            inputData[9] = [1,shape-1,0] #getshape-1 give 0 for P1 and 1 for P2 
        else:
            inputData[9] = [0,shape-1,0]
        return inputData
        
    #translate coordinates to output
    def __translateCTO(y,x):
        dta = [
            [0,1,2],
            [3,4,5],
            [6,7,8]]
    
        return dta[y][x]
   
    #translate output from neural network to coordinates
    def __translateOTC(number):
        dta = [[0,0],[0,1],[0,2],
               [1,0],[1,1],[1,2],
               [2,0],[2,1],[2,2]]
        return dta[number][0],dta[number][1]
    def __win(self,winner):
        if winner == P1:
            self.__b1.addFitness(50)
            self.__b2.remFitness(30)
        else:
            self.__b2.addFitness(50)
            self.__b1.remFitness(30)
        self.__terminateGame()
    def __checkForWin(self,shape):
        board = self.__getBoard().getBoard()
        for y in range(2):
            if board[y] == [shape,shape,shape]: #vannrett skjekk
                return True
        for x in range(2):#loddrett skjekk
            if board[0][x] == board[1][x] and board[2][x] == board[0][x] and board[0][x] == shape:
                return True
        if board[1][1] == shape: #skrå skjekk
            if board[0][0] == shape and board[2][2] == shape:
                return True
            if board[0][2] == shape and board[2][0] == shape:
                return True
        return False



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
        for j in range(10): #find numbers and write them to a list, 3 numbers go into one list
            xData[i].append([])
            valuesConverted = 0

            while valuesConverted < 3:
                try:
                    xData[i][j].append(int(tmpxData[i][c]))
                    valuesConverted += 1
                except:
                    pass
                c += 1

#copy 2D list values to a new 2D list
def copy2DList(listToCopy):
    copiedList = []
    for i in range(len(listToCopy)):
        copiedList.append(listToCopy[i].copy())
    return copiedList                

#gir index for verdien gitt i listen
def getIndex(value,_list):
    for i in range(len(_list)):
        if _list[i] == value:
            return i  

                
def createModel():
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(10,3)))
    model.add(keras.layers.Dense(30,activation='relu'))
    model.add(keras.layers.Dense(270,activation='relu'))
    model.add(keras.layers.Dense(9,activation='softmax'))
    model.compile(optimizer = "adam",loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model