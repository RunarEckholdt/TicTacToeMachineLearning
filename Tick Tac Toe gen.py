# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:42:34 2020

@author: Runar
"""
import random
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np

#todo nytt datasett


loadModel = False
enablePrintBoard = False
epo = 30 #how many epochs
genomesToBreed = 10
matchesPerElimination = 10
population = 30
noMutationChance = 0.9
maxGenerations = 20
generation = 1
maxTurns = 20
amountOfRandomGeneratedGenomes = 5
P1 = 0
P2 = 1

print("Now defining functions...")

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
            
class Bot():
    def __init__(self,player,gen):
        self.__gen = gen
        self.__player = player
        self.__fitness = 100
        self.__piecesLeft = 3
    def addFitness(self,fitnessToAdd):
        self.__fitness += fitnessToAdd
    def remFitness(self,fitnessToRem):
        self.__fitness -= fitnessToRem
    def getFitness(self):
        return self.__fitness
    def piecesLeft(self):
        return self.__piecesLeft
    def mutateGen(self):
        self.__gen = mutateLayers(self.gen)
    def getGen(self):
        return self.__gen
    def predictChoice(self,inputData):
        return self.__gen.predict([inputData])
    def getNr(self):
        return self.__player
    def remPiece(self):
        self.__piecesLeft -= 1
    def resetBot(self):
        self.__fitness = 100
        self.__piecesLeft = 3
    def resetPieces(self):
        self.__piecesLeft = 3
    
        
    
 
   
class game():
    def __init__(self,playBoardIndex,p1Index,p2Index):
        self.playBoardIndex = playBoardIndex
        self.p1Index = p1Index
        self.p2Index = p2Index
        self.turnCounter = 0
        self.gameKilled = False
    def doTurn(self):
        self.botTakeTurn(0,self.p1Index)
        if enablePrintBoard:
            playBoards[self.playBoardIndex].printBoard()
        if self.checkForWin(0,self.p1Index):
            bots[0][self.p1Index].addFitness(50)
            bots[1][self.p2Index].remFitness(20)
            #print("P1 won the game")
            self.gameKilled = True
            return True
        if not self.isFinished():
            self.botTakeTurn(1,self.p2Index)
            if enablePrintBoard:
                playBoards[self.playBoardIndex].printBoard()
            if self.checkForWin(0,self.p1Index):
                bots[1][self.p2Index].addFitness(50)
                bots[0][self.p1Index].remFitness(20)
                #print("P2 won the game")
                self.gameKilled = True
                return True
        self.countTurn()
        bots[0][self.p1Index].remFitness(1)
        bots[1][self.p2Index].remFitness(1)
        self.checkToKillGame()
        return False
    def getValidPrediction(self,bot, index,prediction,predictionSorted,pieceChosen):
         n = len(prediction[0])-1
         predIndex = 0
         while(n>0):
             predIndex = getIndex(predictionSorted[n],prediction[0])
             cords = translateOD2(predIndex)
             y = cords[0]
             x = cords[1]
             if playBoards[self.playBoardIndex].pieceAtPos(y,x) == bot+1 and pieceChosen == False:
                 break
             elif playBoards[self.playBoardIndex].pieceAtPos(y,x) == 0 and pieceChosen == True:
                 break
             else:
                 n -= 1
                 bots[bot][index].remFitness(10)
         return cords
    def botTakeTurn(self,bot,index):
        global playBoards
        if bots[bot][index].piecesLeft() == 0:
            #inputData = copy2DList(playBoards[self.playBoardIndex].getBoard())
            inputData = getInputData(False, bot, self.playBoardIndex)
            #inputData.append([bot+1,0,0])
            prediction = bots[bot][index].predictChoice(inputData)
            predictionSorted = copy2DList(prediction[0])
            predictionSorted = np.sort(predictionSorted)
            cords = self.getValidPrediction(bot,index, prediction, predictionSorted , False)
            sY = cords[0]
            sX = cords[1]
            
        # inputData = copy2DList(playBoards[self.playBoardIndex].getBoard())
        # inputData.append([bot+1,1,0])
        inputData = getInputData(True, bot, self.playBoardIndex)
        prediction = bots[bot][index].predictChoice(inputData)
        predictionSorted = copy2DList(prediction[0])
        predictionSorted = np.sort(predictionSorted)
        try:
            cords = self.getValidPrediction(bot,index, prediction, predictionSorted, True)
            y = cords[0]
            x = cords[1]
            if bots[bot][index].piecesLeft() == 0:
                playBoards[self.playBoardIndex].movePiece(sY,sX,y,x)
            else:
                bots[bot][index].remPiece()
                playBoards[self.playBoardIndex].placePiece(y,x,bot+1)
        except:
            print("Player",bot, "BotIndex",index, "Has failed to move")
            bots[bot][index].remFitness(100)
            self.gameKilled = True
        
        
        
    def countTurn(self):
        self.turnCounter += 1
    def checkToKillGame(self):
        if self.turnCounter > maxTurns:
            self.gameKilled = True
            #print("Game killed because turn counter reached",maxTurns)
    def checkForWin(self,bot,index):
        shape = bot+1
        board = playBoards[self.playBoardIndex].getBoard()
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
    def isFinished(self):
        return self.gameKilled
        

def copy2DList(listToCopy):
    copiedList = []
    for i in range(len(listToCopy)):
        copiedList.append(listToCopy[i].copy())
    return copiedList

def mutateLayers(gen):
    for i in range(1,len(gen.layers)):
        newGen = createModel()
        weights = gen.layers[i].get_weights()
        for k in range(len(weights[0])):
            #print(model.layers[i].get_weights()[j][k])
            
            for l in range(len(gen.layers[i].get_weights()[0][k])):
                r = random.uniform(0,1)
                if r > 0.8:
                    randomMutation = random.uniform(-0.1,0.1)
                    weights[0][k][l] += randomMutation
        for j in range(len(weights[1])):
            r = random.uniform(0,1)
            if r > noMutationChance:
                randomMutation = random.uniform(-0.1,0.1)
                weights[1][j] += randomMutation
        
        newGen.layers[i].set_weights(weights)
    return newGen
        
        
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


def createFirstGenP1():
    global xData
    global yData
    botsP1 = []
    for i in range(population):
        if loadModel:
            gen = keras.models.load_model("modelP1.hdf5")
        else:
            gen = createModel()
            gen.fit(xData,yData,epochs=epo)
        botsP1.append(Bot(0,gen))
    return botsP1

def createFirstGenP2():
    botsP2 = []
    for i in range(population):
        if loadModel:
            gen = keras.models.load_model("modelP2.hdf5")
        else:
            gen = createModel()
            gen.fit(xData,yData,epochs=epo)
        botsP2.append(Bot(1,gen))
    return botsP2

def createBoards():
    playBoards = []
    for i in range(population):
        playBoards.append(Board())
    return playBoards


#translate coordinates to output
def translateOD(y,x):
    dta = [
        [0,1,2],
        [3,4,5],
        [6,7,8]]
    
    return dta[y][x]
   
#translate output from neural network to coordinates
def translateOTC(number):
    dta = [[0,0],[0,1],[0,2],
           [1,0],[1,1],[1,2],
           [2,0],[2,1],[2,2]]
    
    return dta[number]


def getInputData(pieceChosen,player,boardIndex):
    inputData = []
    for i in range(10):
        inputData.append([])
        for j in range(3):
            inputData[i].append([])
    board = playBoards[boardIndex].getBoard()
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

# def addDataToP1(y,x,pieceChosen,board):
#     b = []
#     for i in range(len(board)):
#         b.append(board[i].copy())
#     b.append([pieceChosen,1,0])
#     inputDataP1.append(b)
#     outputDataP1.append(translateOD(y,x))

# def addDataToP2(y,x,pieceChosen,board):
#     b = []
#     for i in range(len(board)):
#         b.append(board[i].copy())
#     b.append([pieceChosen,2,0])
#     inputDataP2.append(b)
#     outputDataP2.append(translateOD(y,x))
    
def getIndex(value,_list):
    for i in range(len(_list)):
        if _list[i] == value:
            return i    
        
        
# def checkForWin(botShape,board):
#     for y in range(2):
#         if board[y] == [botShape,botShape,botShape]: #vannrett skjekk
#             return True
#     for x in range(2):#loddrett skjekk
#         if board[0][x] == board[1][x] and board[2][x] == board[0][x] and board[0][x] == botShape:
#             return True
#     if board[1][1] == botShape: #skrå skjekk
#         if board[0][0] == botShape and board[2][2] == botShape:
#             return True
#         if board[0][2] == botShape and board[2][0] == botShape:
#             return True
#     return False


def setup():
    global bots
    firstGen = True
    #model = createModel()
    readDataAsCsv()
    bots = []
    bots.append(createFirstGenP1())
    bots.append(createFirstGenP2())
    for i in range(maxGenerations):
        if firstGen:
            firstGen = False
        else:
            createNewBots(P1)
            createNewBots(P2)
        runGeneration()
        print("Generation done...")
        print("Highest fitness score P1: ", bots[0][0].getFitness())
        print("Highest fitness score P2: ", bots[1][0].getFitness())
        print("Lowest fitness score P1: ", bots[0][population-1].getFitness())
    superiorGenP1 = bots[0][0].getGen()
    superiorGenP1.save("modelP1.hdf5")
    superiorGenP2 = bots[1][0].getGen()
    superiorGenP2.save("modelP2.hdf5")
    
 
    
def createMatchups():
    p1IndexList = list(range(population))
    p2IndexList = list(range(population))
    games = []
    for i in range(population):
        p1Index = p1IndexList.pop(random.randint(0,len(p1IndexList)-1))
        p2Index = p2IndexList.pop(random.randint(0,len(p2IndexList)-1))
        games.append(game(i,p1Index,p2Index))
    return games


def sortPlayers(players):
    for i in range(len(players)): 
        # Find the minimum element in remaining  
        # unsorted array 
        max_idx = i 
        for j in range(i+1, len(players)): 
            if players[max_idx].getFitness() < players[j].getFitness(): 
                max_idx = j
        # Swap the found minimum element with
        # the first element
        players[i], players[max_idx] = players[max_idx], players[i] 



def runGames():
    global playBoards
    for i in range(matchesPerElimination):
        print("Running match", i+1)
        playBoards = createBoards()
        games = createMatchups()
        gamesFinished = False
        while(not gamesFinished):
            gamesFinished = True
            for i in range(len(games)):
                if not games[i].isFinished():
                    #print("Running turn for game", i)
                    games[i].doTurn()
                    gamesFinished = False
        for i in range(2):
            for j in range(population):
                bots[i][j].resetPieces()

def runGeneration():
    global generation
    print("running generation:", generation)
    runGames()
    sortPlayers(bots[0])
    sortPlayers(bots[1])
    generation = generation + 1

def createNewBots(p):
    newBotTempList = []
    topGenomes = []
    for i in range(genomesToBreed):
        bots[p][i].resetBot()
        topGenomes.append(bots[p][i].getGen())
    newBotTempList = manageBreeding(topGenomes,p)
    for i in range(genomesToBreed):
        newBotTempList.append(bots[p][i])
    for i in range(population-genomesToBreed*2 - amountOfRandomGeneratedGenomes):
        gen = mutateLayers(topGenomes[0])
        newBotTempList.append(Bot(p,gen))
    for i in range(amountOfRandomGeneratedGenomes):
        newBotTempList.append(Bot(p,createRandomGen()))
    bots[p] = newBotTempList
    



        

def manageBreeding(genList,p):
    breededBots = []
    for i in range(1,genomesToBreed):
        gen = createModel()
        breededBots.append(breed(genList[0],genList[i],gen,p))
    gen = createModel()
    breededBots.append(breed(genList[1],genList[2],gen,p))
    return breededBots

def breed(gen1, gen2,targetGen,p):
    for i in range(1,len(targetGen.layers)):
        for j in range(len(targetGen.layers[i].get_weights())):
            for k in range(len(targetGen.layers[i].get_weights()[0][j])):
                r = random.uniform(0,1)
                if r > 0.5:
                    targetGen.layers[i].get_weights()[0][j][k] = gen1.layers[i].get_weights()[0][j][k]
                else:
                    targetGen.layers[i].get_weights()[0][j][k] = gen2.layers[i].get_weights()[0][j][k]
                
        for j in range(len(targetGen.layers[i].get_weights()[1])):
            r = random.uniform(0,1)
            if r > 0.5:
                targetGen.layers[i].get_weights()[1][j] = gen1.layers[i].get_weights()[1][j]
            else:
                targetGen.layers[i].get_weights()[1][j] = gen2.layers[i].get_weights()[1][j]
    return Bot(p,targetGen)
 
def createRandomGen():
    gen = createModel()
    
    for i in range(1,len(gen.layers)):
        for j in range(len(gen.layers[i].get_weights())):
            for k in range(len(gen.layers[i].get_weights()[0][j])):
                r = random.uniform(-1,1)
                gen.layers[i].get_weights()[0][j][k] = r
                
                
                
        for j in range(len(gen.layers[i].get_weights()[1])):
            r = random.uniform(-1,1)
            gen.layers[i].get_weights()[1][j] = r
    return gen










print("Starting the setup...")
setup()    




    
    
    
    
    
    
    
    
    
    
    
    
    
    




        