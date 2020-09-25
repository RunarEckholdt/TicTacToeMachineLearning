# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 22:44:04 2020

@author: Runar
"""

import BoardModule as boardm
import numpy as np

P1 = 0
P2 = 1

class Game():
    def __init__(self,b1,b2, 
                 maxTurns = 20, 
                 blockReleasePunishment = 30, 
                 blockReward = 20,
                 winReward = 40):
        self.__b1 = b1
        self.__b2 = b2
        self.__board = boardm.Board()
        self.__turnCounter = 0
        self.__finished = False
        self.__maxTurns = maxTurns
        self.__blockReleasePunishment = blockReleasePunishment
        self.__blockReward = blockReward
        self.__winReward = winReward
    def __getBoard(self):
        return self.__board
    def getP1(self):
        return self.__b1
    def getP2(self):
        return self.__b2
    def isFinished(self):
        return self.__finished
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
        if self.__turnCounter == self.__maxTurns:
            #print("Game reached turn 30 and is beeing terminated")
            self.__terminateGame()
            
    def __terminateGame(self):
        self.__finished = True
    def __takeTurn(self,bot):
        
        #if bot must choose a piece
        if bot.piecesLeft() == 0:
            mustChoosePiece = True
        else:
            mustChoosePiece = False
        
        if mustChoosePiece:
            inputData1 = self.__getInputData(False,bot.getShape())
            prediction = bot.predictChoice(inputData1)
            predictionSorted = np.sort(copy2DList(prediction)) #kopierer prediction og sorterer listen
            bot, y1, x1 = self.__getValidPrediction(bot, prediction, predictionSorted, False)
        inputData2 = self.__getInputData(True,bot.getShape())
        prediction = bot.predictChoice(inputData2)
        predictionSorted = np.sort(copy2DList(prediction))
        bot,y2,x2 = self.__getValidPrediction(bot, prediction, predictionSorted, True)
        #try:
        if mustChoosePiece:
            self.__getBoard().movePiece(y1,x1,y2,x2)
            if self.__checkIfBOrR(y1, x1, bot.getShape(),release=True):
                bot.remFitness(self.__blockReleasePunishment)
        else:
            bot.remPiece()
            self.__getBoard().placePiece(y2,x2,bot.getShape())
            if self.__checkIfBOrR(y2, x2, bot.getShape(),release=False):
                bot.addFitness(self.__blockReward)
        # except:
        #     print("Bot has failed to move, game is terminated")
        #     bot.remFitness(100)
        #     self.__terminateGame()
        return bot
            
    def __getValidPrediction(self,bot,prediction,predictionSorted,pieceChosen):
        n = len(prediction)-1
        predIndex = 0
        shape = bot.getShape()
        board = self.__getBoard()
        while(n>0):
            predIndex = getIndex(predictionSorted[n],prediction)
            y,x = self.__translateOTC(predIndex)
            
            #is piece is not chosen and it picks it's own piece
            if board.pieceAtPos(y,x) == shape and pieceChosen == False:
                break
            #if piece is chosen and position is empty
            elif board.pieceAtPos(y,x) == 0 and pieceChosen == True:
                break
            #den faila en predict
            else:
                n -= 1
                bot.remFitness(20)
        if y == None:
            print("Y was not set")
        return bot, y, x
    
    
    def __getInputData(self,pieceChosen,shape):
        inputData = []
        for i in range(10):
            inputData.append([])
            for j in range(3):
                inputData[i].append([])
        board = self.__getBoard().getBoard()
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
    
    #check if block or realease
    def __checkIfBOrR(self,y,x,shape,release):
        if release:
            shape = 0
        if shape == 1:
            riv = 2
        else:
            riv = 1
        board = self.__getBoard().getBoard().copy()
        board = np.array(board)
        row = board[y]
        row = row[row!=shape]
        colum = board[:, x]
        colum = colum[colum!=shape]
        inDigSky = False
        inDigGrav = False
        
        if x == y:
            inDigGrav = True
        if y == 0 and x == 2 or y == x or y == 3 and x == 0:
            inDigSky = True
        
        digSky = np.zeros(3)
        digGrav = np.zeros(3)
        
        
        
        if inDigGrav:
            for i in range(3):
                digGrav[i] = board[i][i]
            digGrav = digGrav[digGrav != shape]
        if inDigSky: #lager en array på diagonalen
            for i,(y,x) in enumerate(((2,0),(1,1),(0,2))):
                digSky[i] = board[y][x]
            digSky = digSky[digSky != shape]
        
        #horizontal check
        if len(row) == 2:
            if row[0]==riv and any(i == row[0] for i in row):
                return True

        #vertical check
        if len(colum) == 2:
            if colum[0]==riv and any(i == colum[0] for i in colum):
                return True

        #diagonal check from bottom left
        if inDigSky and len(digSky) == 2:
            if digSky[0]==riv and any(i == digSky[0] for i in digSky): 
                return True

        #diagonal check from upper left
        if inDigGrav and len(digGrav) == 2:
            if digGrav[0]==riv and any(i == digGrav[0] for i in digGrav):
                return True

        return False
        
        
        
        
        
        
    #translate coordinates to output
    def __translateCTO(self,y,x):
        dta = [
            [0,1,2],
            [3,4,5],
            [6,7,8]]
    
        return dta[y][x]
   
    #translate output from neural network to coordinates
    def __translateOTC(self,number):
        dta = [[0,0],[0,1],[0,2],
               [1,0],[1,1],[1,2],
               [2,0],[2,1],[2,2]]
        return (dta[number][0],dta[number][1])
    
    def __win(self,winner):
        if winner == P1:
            self.__b1.addFitness(self.__winReward)
        else:
            self.__b2.addFitness(self.__winReward)
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
    
    
    
