# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 22:41:56 2020

@author: Runar
"""

from tensorflow import keras
import threading
import random

kerasMutex = threading.Lock()

class Bot():
    def __init__(self,P,model,noMutationChance = 0.9):
        self.__P = P+1
        self.__model = model
        self.__piecesLeft = 3
        self.__fitness = 100
        self.__noMutationChance = noMutationChance
    def addFitness(self,fitnessToAdd):
        self.__fitness += fitnessToAdd
    def remFitness(self,fitnessToRem):
        self.__fitness -= fitnessToRem
    def getFitness(self):
        return self.__fitness
    def piecesLeft(self):
        return self.__piecesLeft
    def mutateModel(self):
        self.__model = self.__mutateLayers(self.__model)
    def getGen(self):
        return self.__model
    def predictChoice(self,inputData):
        prediction = self.__model.predict([inputData])
        return prediction[0]
    def getShape(self):
        return self.__P
    def remPiece(self):
        self.__piecesLeft -= 1
    def resetPieces(self):
        self.__piecesLeft = 3
    def __mutateLayers(self,gen):
        newGen = threadProtectedKerasClone(gen)
        for i in range(1,len(gen.layers)):
            weights = gen.layers[i].get_weights()
            for k in range(len(weights[0])):
                #print(model.layers[i].get_weights()[j][k])
            
                for l in range(len(gen.layers[i].get_weights()[0][k])):
                    r = random.uniform(0,1)
                    if r > self.__noMutationChance:
                        randomMutation = random.uniform(-0.1,0.1)
                        weights[0][k][l] += randomMutation
            for j in range(len(weights[1])):
                r = random.uniform(0,1)
                if r > self.__noMutationChance:
                    randomMutation = random.uniform(-0.1,0.1)
                    weights[1][j] += randomMutation
                                
                newGen.layers[i].set_weights(weights)
        return newGen
    def getModel(self):
        return self.__model
    
    


#protect the clone_model function from beeing used by both threads at the same time
def threadProtectedKerasClone(modelToClone):
        kerasMutex.acquire()
        clone = keras.models.clone_model(modelToClone)
        kerasMutex.release()
        return clone
    
    
def createModel():
        kerasMutex.acquire()
        model = keras.Sequential()
        model.add(keras.layers.Flatten(input_shape=(10,3)))
        model.add(keras.layers.Dense(30,activation='relu'))
        model.add(keras.layers.Dense(270,activation='relu'))
        model.add(keras.layers.Dense(9,activation='softmax'))
        model.compile(optimizer= "adam",loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        kerasMutex.release()
        return model
    
    
    