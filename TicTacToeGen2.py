
import GenerationModule as genm


# #settings
P1 = 0
P2 = 1
# doPrintBoard = False
# loadModel = True
# mutatedBots = 20
# breededBots = 10
# keptBots = 10
# noMutationChance = 0.9
# population = mutatedBots + breededBots + keptBots
# epo = 40
# maxTurns = 20
# debug = False
# maxGens = 100
# matchesPerGeneration = 3
# restrictLastMoved = True

# #rewards
# winReward = 30
# blockReward = 20
# blockReleasePunishment = 40





class GenEvolution():
    def __init__(self,maxGenerations = 40):
        self.__maxGenerations = maxGenerations
    def runGens(self,isTest=False):
        generation = genm.Generation(1)
        oldBots = generation.runGeneration()
        del generation
        for i in range(2,self.__maxGenerations+1):
            generation = genm.Generation(i,oldBots)
            oldBots = generation.runGeneration()
            del generation
        print("Genetic Evolution complete...")
        modelP1 = oldBots[P1][0].getModel()
        modelP2 = oldBots[P2][0].getModel()
        
        if not isTest:
            print("Saving superior model for P1...")
            modelP1.save("modelP1.hdf5")
            print("Saving superior model for P2...")
            modelP2.save("modelP2.hdf5")
        
        
        
    
             


evol = GenEvolution(maxGenerations=1)
evol.runGens(isTest=True)













