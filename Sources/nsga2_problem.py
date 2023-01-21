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
        ini_gene = [1,5,3,2,1]
        
        for i in range(self.num_of_variables):
            tmp = np.random.random()
            if tmp < 0.33:
                ini_gene[i] += 1
                if ini_gene[i] > self.variables_range[0][1]:
                    ini_gene[i] = self.variables_range[0][1]
            elif tmp < 0.67:
                ini_gene[i] -= 1
                if ini_gene[i] < self.variables_range[0][0]:
                    ini_gene[i] = self.variables_range[0][0]
        
        individual.features = ini_gene
        return individual
    
    def calculate_objectives(self, individual):
        if self.expand:
            individual.objectives = [f(*individual.features) for f in self.objectives]
        else:
            individual.objectives = [f(individual.features) for f in self.objectives]