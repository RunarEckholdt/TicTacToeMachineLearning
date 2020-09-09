# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:35:29 2020

@author: Runar
"""

import random
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
import threading



# def createModel():
#     model = keras.Sequential()
#     model.add(keras.layers.Flatten(input_shape=(4,3)))
#     model.add(keras.layers.Dense(12,activation='relu'))
#     model.add(keras.layers.Dense(9,activation='softmax'))
#     model.compile(optimizer = "Gradient_Decent",loss="mean_squared_error", metrics=["accuracy"])
#     return model
    
    
    

# def readDataAsCsv():
#     global yData
#     global xData
#     yData = []
#     xData = []
#     loadedData = pd.read_csv("tictactoe.csv")
#     tmpyData = list(loadedData['output'].values)
#     tmpxData = list(loadedData['input'].values)
    
#     for i in range(len(tmpyData)):
#         yData.append(int(tmpyData[i]))
    
#     for i in range(len(tmpxData)):
#         xData.append([])
#         for j in range(4):
#             xData[i].append([])
#             valuesConverted = 0
#             c = 0
#             while valuesConverted < 3:
#                 try:
#                     xData[i][j].append(int(tmpxData[i][c]))
#                     valuesConverted += 1
#                 except:
#                     pass
#                 c += 1
                
                
# readDataAsCsv()
# model1 = createModel()
# model2 = createModel()
#print(model.layers)

# model1.fit(xData,yData, epochs = 30)

#print(model.layers)

# print(model1.layers[1].get_weights()[0][0])
# print(model2.layers[1].get_weights()[0][0])
#print(model.layers[1].get_weights()[0][0])


# def mutateLayers():
#     global model
#     for i in range(1,len(model.layers)):
#         weights = model.layers[i].get_weights()
#         for k in range(len(weights[0])):
#             #print(model.layers[i].get_weights()[j][k])
            
#             for l in range(len(model.layers[i].get_weights()[0][k])):
#                 r = random.uniform(0,1)
#                 if r > 0.8:
#                     randomMutation = random.uniform(-0.1,0.1)
#                     weights[0][k][l] += randomMutation
#         for j in range(len(weights[1])):
#             r = random.uniform(0,1)
#             if r > 0.8:
#                 randomMutation = random.uniform(-0.1,0.1)
#                 weights[1][j] += randomMutation
        
#         model.layers[i].set_weights(weights)
                
            
#mutateLayers()

#print(model.layers[1].get_weights()[0][0])

def p(text):
    for i in range(500):
            print(text)

class pThread(threading.Thread):
    def __init__(self,text):
        threading.Thread.__init__(self)
        self.text=text
    def run(self):
        p(self.text)
    


    
th1 = pThread("Kake")
th2 = pThread("Banan")

th1.start()
th2.start()












