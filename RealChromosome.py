'''
Created on 14 mar. 2020

@author: George
'''

from random import randint


class Chromosome:
    def __init__(self, problParam = None):
        '''
        Locus-based representation of the network
        division 
        '''
        self.__problParam = problParam
        self.__net = problParam['network']['mat']
        
        self.__repres = self.generateFromNeighbors()
        
        self.__fitness = 0.0
    
    def generateFromNeighbors(self):
        '''
        We will generate the representants of the generations by linking each node to one of its neighbors (if any)
        
        First, we consider an empty list of representants.
        Then, we iterate the list of vertices and for each vertex we form its list of neighbors from which we randomly choose one.
        Each chosen neighbor is saved in the "repres" list.
        
        This procedure ensures that all the data is correct and all the offsprings will also be correct.
        '''
        repres = []
        for i in range(0, self.__problParam['vertices']):
            neighs = []
            for j in range(0, self.__problParam['vertices']):
                if self.__net[i][j] == 1:
                    neighs.append(j)
            
            if(len(neighs)) == 0: # no neighbors
                randomNeighbor = None
            else:
                randomNeighbor = neighs[randint(0,len(neighs)-1)] # randomly choose one of the neighbors
            repres.append(randomNeighbor) 
        
        return repres
    
    
    @property
    def repres(self):
        return self.__repres
    
    @property
    def fitness(self):
        return self.__fitness 
    
    @repres.setter
    def repres(self, l = []):
        self.__repres = l 
    
    @fitness.setter 
    def fitness(self, fit = 0.0):
        self.__fitness = fit 
    
    def crossover(self, c): # Standard uniform crossover
        mask = [randint(0, 1) for _ in range(0, len(self.__repres))]
        
        M = self.__repres
        F = c.__repres
        
        newrepres = [ M[i] if mask[i]==0 else F[i] for i in range(0, len(self.__repres)) ]
        
        offspring = Chromosome(c.__problParam)
        offspring.repres = newrepres
        
        return offspring
    
    def mutation(self):
        '''
        A variant adopted by [48] is to assign a node to the
        cluster of one of its neighbors, while in [58] the majority
        label of the neighbors is adopted.
        
        '''
        pos = randint(0, len(self.__repres) - 1)
        
        neighs = []
        A = self.__net
        for j in range(0, len(self.__repres)):
            if A[pos][j] == 1:
                neighs.append(j)
        
        if len(neighs) == 0:
            return
        self.__repres[pos] = neighs[randint(0, len(neighs)-1)]
        
        #self.repair() - already repaired in this case (always choosing an existing neighbor)
        
        
    def __str__(self):
        return '\nChromo: ' + str(self.__repres) + ' has fit: ' + str(self.__fitness)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, c):
        return self.__repres == c.__repres and self.__fitness == c.__fitness

