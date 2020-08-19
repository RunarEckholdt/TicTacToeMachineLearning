# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 20:03:59 2020

@author: Runar
"""

import neat
import os


def setup():
    global config
    global population
    configFile = "NeatConfig.txt"
    localDir = os.path.dirname(__file__)
    configPath = os.path.join(localDir, configFile)
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultSpeciesSet,neat.DefaultReproduciton,
                                neat.DefaultStagnation, configPath)
    population = neat.Population(config)
    

