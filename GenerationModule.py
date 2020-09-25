# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 22:46:27 2020

@author: Runar
"""

import GameModule as gm
import time
import threading
import pandas as pd
from tensorflow import keras
import BotModule as bm
import random

P1 = 0
P2 = 1


class Generation():
    def __init__(self,
                 genNr,
                 oldBots = None,
                 matchesPerGeneration = 3,
                 loadModel = True,
                 epo = 40,
                 keptBots = 10,
                 mutatedBots = 20,
                 breededBots = 10):
        
        
        self.__oldBots = oldBots
        self.__genNr = genNr
        self.__bots = [[],[]]
        self.__bestModelsP1 = []
        self.__bestModelsP2 = []
        self.__loadModel = loadModel
        self.__matchesPerGeneration = matchesPerGeneration
        self.__population = keptBots+mutatedBots+breededBots
        self.__epo = epo
        self.__keptBots = keptBots
        self.__mutatedBots = mutatedBots
        self.__breededBots = breededBots
        
        
        if self.__genNr == 1 and self.__loadModel:
            self.__loadFirstGenBots()
        elif self.__genNr == 1:
            self.__createFirstGenBots()
        else:
            self.__createNewGenBots()
        self.__fetchBestModels()
        
        
    def runGeneration(self):
        print("---------------------------------")
        print("Running generation", self.__genNr)
        start = time.time()
        for i in range(self.__matchesPerGeneration):
            self.__createMatches(i)
            self.__runMatches()
            self.__fetchBots()
        end = time.time()
        diff = end-start
        print("Matches took %.3f s"%diff)
        self.__bots[P1] = self.__sortBots(self.__bots[P1])
        self.__bots[P2] = self.__sortBots(self.__bots[P2])
        print("Best P1 fitness score = ", self.__bots[P1][0].getFitness())
        print("Best P2 fitness score = ", self.__bots[P2][0].getFitness())
        self.__bots[P1][0].getModel().save("tmpModelP1.hdf5")
        self.__bots[P2][0].getModel().save("tmpModelP2.hdf5")
        return self.__bots
        
    def __fetchBestModels(self):
        if self.__genNr == 1:
            for i in range(self.__matchesPerGeneration):
                self.__bestModelsP1.append(self.__bots[P1][i].getModel())
                self.__bestModelsP2.append(self.__bots[P2][i].getModel())
        else:    
            for i in range(self.__matchesPerGeneration):
                self.__bestModelsP1.append(self.__oldBots[P1][i].getModel())
                self.__bestModelsP2.append(self.__oldBots[P1][i].getModel())
        for i in range(self.__matchesPerGeneration):
            self.__bestModelsP1[i]._make_predict_function()
            self.__bestModelsP2[i]._make_predict_function()
        
    def __loadFirstGenBots(self):
        P1s = []
        P2s = []
        for i in range(self.__population):
            p1Model = keras.models.load_model("modelP1.hdf5",compile=False)
            p2Model = keras.models.load_model("modelP2.hdf5",compile=False)
            P1s.append(bm.Bot(P1,p1Model))
            P2s.append(bm.Bot(P2,p2Model))
            if i != 0:
                P1s[i].mutateModel()
                P2s[i].mutateModel()
        self.__bots[P1] = P1s
        self.__bots[P2] = P2s
            
    
                    
    def __createFirstGenBots(self):
        P1s = []
        P2s = []
        xData,yData = readDataAsCsv()
        for i in range(self.__population):
            modelP1 = bm.createModel()
            modelP1.fit(xData,yData,epochs=self.__epo)
            modelP2 = bm.createModel()
            modelP2.fit(xData,yData,epochs=self.__epo)
            P1s.append(bm.Bot(P1,modelP1))
            P2s.append(bm.Bot(P2,modelP2))
        self.__bots[P1] = P1s
        self.__bots[P2] = P2s
            
    def __createNewGenBots(self):
        start = time.time()
        th1 = threading.Thread(target=self.__createNewGenBotsTh,args=(P1,))
        th2 = threading.Thread(target=self.__createNewGenBotsTh,args=(P2,))
        th1.start()
        th2.start()
        th1.join()
        th2.join()
        end = time.time()
        diff = end - start
        print("CreateNewGenBots took %.2f sek" %diff)
        
        
        
    def __createNewGenBotsTh(self,p):
        self.__bots[p].extend(self.__cloneLastGenBots(p))
        self.__bots[p].extend(self.__manageBreeding(p))
        self.__bots[p].extend(self.__createMutants(p))
        
        
    def __cloneLastGenBots(self,p):
        clonedBots = []
        for i in range(self.__keptBots):
            model = self.__oldBots[P1][i].getModel()
            model = bm.threadProtectedKerasClone(model)
            clonedBots.append(bm.Bot(p,model))
        return clonedBots
        
    def __createMutants(self,p):
        mutants = []
        for i in range(self.__mutatedBots):
            model = bm.threadProtectedKerasClone(self.__bots[p][0].getModel())#clone the best version of the last gen bots
            bot = bm.Bot(p,model)
            bot.mutateModel()
            mutants.append(bot)
        return mutants
        
    def __manageBreeding(self,p):
        bBots = []
        for i in range(1,self.__breededBots):
            bBots.append(self.__breed(self.__oldBots[p][0].getModel(),self.__oldBots[p][i].getModel(),p))
        bBots.append(self.__breed(self.__oldBots[p][1].getModel(),self.__oldBots[p][2].getModel(),p))
        return bBots
    #take two models and randomly merges them into a new model
    def __breed(self,model1, model2,p):
        targetModel = bm.createModel()
        for i in range(1,len(targetModel.layers)):
            #weights
            for j in range(len(targetModel.layers[i].get_weights())):
                for k in range(len(targetModel.layers[i].get_weights()[0][j])):
                    r = random.uniform(0,1)
                    if r > 0.5:
                        targetModel.layers[i].get_weights()[0][j][k] = model1.layers[i].get_weights()[0][j][k]
                    else:
                        targetModel.layers[i].get_weights()[0][j][k] = model2.layers[i].get_weights()[0][j][k]
            #bias    
            for j in range(len(targetModel.layers[i].get_weights()[1])):
                r = random.uniform(0,1)
                if r > 0.5:
                    targetModel.layers[i].get_weights()[1][j] = model1.layers[i].get_weights()[1][j]
                else:
                    targetModel.layers[i].get_weights()[1][j] = model2.layers[i].get_weights()[1][j]
        return bm.Bot(p,targetModel)
        
    
    
    def __createMatches(self,matchNr):
        P1s = self.__bots[P1]
        P2s = self.__bots[P2]
        matches = [[],[]]
        for j in range(self.__population):
            model1 = P1s[matchNr].getModel()
            model2 = P2s[matchNr].getModel()
            p1 = bm.Bot(P1, model1)
            p2 = bm.Bot(P2, model2)
            matches[P1].append(gm.Game(P1s[j],p2))
            matches[P2].append(gm.Game(p1,P2s[j]))
        self.__matches = matches
    
    def __runMatches(self):
        th1P1 = threading.Thread(target=self.__runMatchesTh,args=(0,19,P1,))
        th2P1 = threading.Thread(target=self.__runMatchesTh,args=(20,39,P1))
        th1P2 = threading.Thread(target=self.__runMatchesTh,args=(0,19,P2,))
        th2P2 = threading.Thread(target=self.__runMatchesTh,args=(20,39,P2))
        
        th1P1.start()
        th2P1.start()
        th1P2.start()
        th2P2.start()
        
        th1P1.join()
        th2P1.join()
        th1P2.join()
        th2P2.join()
    
    def __runMatchesTh(self,start,stop,p):
        done = False
        while not done:
            done = True
            for i in range(start,stop+1):
                if not self.__matches[p][i].isFinished():
                    self.__matches[p][i].doTurn()
                    done = False
    
    def __fetchBots(self):
        bots = [[],[]]
        for i in range(self.__population):
            bots[P1].append(self.__matches[P1][i].getP1())
            bots[P2].append(self.__matches[P2][i].getP2())
            bots[P1][i].resetPieces()
            bots[P2][i].resetPieces()
        self.__bots = bots
        
    
    
        
        
    def __sortBots(self,bots):
        for i in range(len(bots)): 
            # Find the minimum element in remaining  
            # unsorted array 
            max_idx = i 
            for j in range(i+1, len(bots)): 
                if bots[max_idx].getFitness() < bots[j].getFitness(): 
                    max_idx = j
                    # Swap the found minimum element with
                    # the first element
                    bots[i], bots[max_idx] = bots[max_idx], bots[i] 
        return bots
    
    
    
    
def readDataAsCsv():
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
    return xData,yData
    