#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import time
import random
import math
from model.control import Control
from model.map import maps
from drawing.display import Display
from drawing.box import Box
from model.box import Box as cube
import pygame
from copy import deepcopy


def print_stack(stack, algorithm):
    if algorithm == "dfs":
        print("STACK: ")
    elif algorithm == "bfs":
        print("QUEUE: ")

    for state in stack:
        print("( %s ) " % state[0])


# Number of individuals in each generation
POPULATION_SIZE = 200
MAX_LEN = 100
PROBABLE = 0.3
# Valid genes
GENES = 'LRUD'


class Individual(object):
    def __init__(self, chromosome, state: Control):
        # self.initState = state.get_state()
        self.state = state
        self.chromosome = chromosome
        self.trimString()
        self.fitness = self.cal_fitness()
    @classmethod
    def mutated_genes(self):
        global GENES
        gene = random.choice(GENES)
        return gene

    @classmethod
    def create_gnome(self):
        '''
        create chromosome or string of genes
        '''
        global MAX_LEN
        gnome_len = MAX_LEN
        return [self.mutated_genes() for _ in range(gnome_len)]
    def selfMate(self):
        child_chromosome = deepcopy(self.chromosome)
        while len(child_chromosome) < MAX_LEN:
            child_chromosome.append(self.mutated_genes())
        return Individual(child_chromosome, self.state)

    def mate(self, par2):
        '''
        Perform mating and produce new offspring
        '''

        # chromosome for offspring
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):

            prob = random.random()

            # if prob is less than 0.45, insert gene
            # from parent 1
            if (prob < PROBABLE)  :
                child_chromosome.append(gp1)

                # if prob is between 0.45 and 0.90, insert
                # gene from parent 2
            elif prob < PROBABLE*2 :
                child_chromosome.append(gp2)

                # otherwise insert random gene(mutate),
                # for maintaining diversity
            else:
                child_chromosome.append(self.mutated_genes())
        while len(child_chromosome) < MAX_LEN:
            child_chromosome.append(self.mutated_genes())
                # create new Individual(offspring) using
                # generated chromosome for offspring
        return Individual(child_chromosome, self.state)

    def cal_fitness(self):
        # print ("=================== beginning ===============")
        # print ("=================== beginning ===============")
        # print ("=================== beginning ===============")
        # print ("".join(self.chromosome))
        global MAX_LEN
        countLive = 0
        result = True
        current_state = self.state.get_state()
        current_maps = self.state.get_maps()
        # print ("=================== beginning ===============")
        # # print (self.state.current)
        # state = deepcopy(self.state)
        # # print (self.state.current)
        # # state = self.state
        # print ("================== end ===============")
        for i in range(len(self.chromosome)):
            c = self.chromosome[i]
            if c== 'U':
                result = self.state.move_up()
            elif c== 'D':
                result = self.state.move_down()
            elif c== 'R':
                result = self.state.move_right()
            elif c== 'L':
                result = self.state.move_left()
            countLive += 1
            if self.state.check_goal():
                print(self.state.current)
                self.chromosome = self.chromosome[:i+1]
                self.state.set_state(current_state, current_maps)
                return 0
            if result == False:
                self.chromosome = self.chromosome[:i] 
                break 

        temptResult = MAX_LEN - countLive+1

        x1, y1 = self.state.maps.end
        x2, y2 = self.state.maps.current_box.location[0]
        distant2 = self.state.maps.distantToTarget(x2, y2)
        if len(self.state.maps.current_box.location) >1:
            x3, y3 = self.state.maps.current_box.location[1]
            distant3 = self.state.maps.distantToTarget(x2, y2)
            distant2 = (distant2+distant3)/2
            x2 = (int(x2)+int(x3)/2)
            y2 = (int(y2)+int(y3)/2)
        distant = abs(int(x1)-int(x2)) + abs(int(y1)-int(y2))
        
        self.state.set_state(current_state, current_maps)
        return  distant2*10  + distant*3 + temptResult
    def trimString(self):
        stringChr = "".join(self.chromosome)
        while stringChr.find('UD') != -1 or stringChr.find('DU') != -1 or stringChr.find('RL') != -1 or stringChr.find('LR') != -1:
            stringChr = stringChr.replace('UD', '')
            stringChr = stringChr.replace('DU', '')
            stringChr = stringChr.replace('RL', '')
            stringChr = stringChr.replace('LR', '')
        self.chromosome = [i for i in stringChr]
    def getPath(self):
        path = [self.state.start ]
        for i in range(len(self.chromosome)):
            c = self.chromosome[i]
            if c== 'U':
                result = self.state.move_up()
            elif c== 'D':
                result = self.state.move_down()
            elif c== 'R':
                result = self.state.move_right()
            elif c== 'L':
                result = self.state.move_left()

            path.append(self.state.current)
        return path
def geneticAlgorism(state: Control):
    global POPULATION_SIZE 
    initState = state.get_state()
    initMap = state.get_maps()
    # current generation
    generation = 1
    found = False
    population = []

    # create initial population
    while len(population) < POPULATION_SIZE:
        gnome = Individual.create_gnome()
        state.set_state(initState, initMap)
        population.append(Individual(gnome, state))

    while not found:
        # sort the population in increasing order of fitness score
        population = sorted(population, key=lambda x: x.fitness)

        if population[0].fitness <= 0:
            # print("".join(population[0].chromosome))
            population[0].trimString()
            return population[0].getPath()
            found = True
            break

        new_generation = []

        s = int((5*POPULATION_SIZE)/100)
        new_generation.extend(population[:s])

        for i in range(s):
            new_generation.append(new_generation[i].selfMate())



        while len(new_generation) < POPULATION_SIZE:
            parent1 = random.choice(population[:80])
            parent2 = random.choice(population[:80])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation

        print("Generation: {}\tString: {}\tFitness: {}".
              format(generation,
                     "".join(population[0].chromosome),
                     population[0].fitness))

        generation += 1
