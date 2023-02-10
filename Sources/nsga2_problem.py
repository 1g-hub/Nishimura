from nsga2_individual import Individual
import random
import numpy as np


class Problem:

    def __init__(self, objectives, num_of_variables, variables_range, expand=True, same_range=False):
        self.num_of_objectives = len(objectives)
        self.num_of_variables = num_of_variables
        self.objectives = objectives
        self.expand = expand
        self.variables_range = []
        if same_range:
            for _ in range(num_of_variables):
                self.variables_range.append(variables_range[0])
        else:
            self.variables_range = variables_range
    '''
    def generate_individual(self):
        individual = Individual()
        individual.features = [random.uniform(*x) for x in self.variables_range]
        return individual
    '''

    def generate_individual(self):
        individual = Individual()
        '''
        ini_gene = [
            4,4,1,#0
            1,1,5 #14
            ]
            '''
        
        ini_gene = [
                4,4,1,#0
                2,2,2,#1
                3,3,3,#2
                4,3,4,#3
                5,4,5,#4
                2,2,2,#5
                2,3,3,#6
                1,1,1,#7
                1,3,2,#8
                2,1,2,#9
                3,1,3,#10
                1,2,2,#11
                2,3,3,#12
                1,1,1,#13
                1,1,5 #14
            ]

        deck = []

        for i in range(self.num_of_variables):
            deck.append(random.randint(self.variables_range[0][0], self.variables_range[0][1]))
        '''
        '''
        
        individual.features = deck
        #print(individual.features)
        return individual
    
    def calculate_objectives(self, individual):
        if self.expand:
            individual.objectives = [f(*individual.features) for f in self.objectives]
        else:
            individual.objectives = [f(individual.features) for f in self.objectives]