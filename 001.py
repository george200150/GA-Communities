'''
Created on 14 mar. 2020

@author: George
'''

from GA import GA
import numpy as np 
import networkx as nx
import matplotlib.pyplot as plt
import warnings
from random import seed
from random import randint
from utils import loadNet
from utils import detComunitati


def convert1to2():
    #f = open("karate.in", "r")
    #f = open("dolphins.in", "r")
    f = open("football.in", "r")
    #f = open("krebs.in", "r")
    allLines = f.read()
    lines = allLines.split('\n')
    lineParts = [ line.split(' ') for line in lines]
    
    maxN = 0
    listInc = []
    for tup in lineParts:
        src = int(tup[0])
        dst = int(tup[1])
        listInc.append([src, dst])
        maxN = max(src, dst, maxN)
    N = maxN + 1
    M = len(lines)
    A = []
    for _ in range(N):
        lst = []
        for _ in range(N):
            lst.append(0)
        A.append(lst)
    
    for lst in listInc:
        src = lst[0]
        dst = lst[1]
        A[src][dst] = 1
        A[dst][src] = 1
    
    f.close()
    g = open('net.in', 'w')
    g.write(str(N) + "\n")
    
    for line in A:
        for elem in line:
            g.write(str(elem) + " ")
        g.write("\n")
    g.close()










def plotAFunction(xref, yref, x, y, xoptimal, yoptimal, message):    
    plt.plot(xref, yref, 'b-')
    plt.plot(x, y, 'ro', xoptimal, yoptimal, 'bo')
    plt.title(message)
    plt.show()
    plt.pause(0.9)
    plt.clf()

# plot the network 
def plotRawNetwork(net):
    warnings.simplefilter('ignore')
    
    A=np.matrix(net) # network["mat"]
    G=nx.from_numpy_matrix(A)
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 8)) 
    nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.cm.RdYlBu)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.show(G)

# plot a particular division in communities
def plotCommunities(communities, network):
    
    A=np.matrix(network["mat"])
    G=nx.from_numpy_matrix(A)
    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(10, 10))  # image is 8 x 8 inches 
    nx.draw_networkx_nodes(G, pos, node_size = 600, cmap = plt.cm.RdYlBu, node_color = communities)
    nx.draw_networkx_edges(G, pos, alpha = 0.3)
    plt.show(G)







# evaluate the quality of previous communities inside a network
# https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/modularity.pdf
def modularity(communities, param):
    noNodes = param['noNodes']
    mat = param['mat']
    degrees = param['degrees']
    noEdges = param['noEdges']  
    M = 2 * noEdges
    Q = 0.0
    for i in range(0, noNodes):
        for j in range(0, noNodes):
            if (communities[i] == communities[j]):
                Q += (mat[i][j] - degrees[i] * degrees[j] / M)
    return Q * 1 / M







# http://staff.fmi.uvt.ro/~daniela.zaharie/ma2019/Projects/Applications/communities_detection/GA_NET.pdf
# https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/modularity.pdf
# http://staff.icar.cnr.it/pizzuti/pubblicazioni/IEEETEC2017.pdf
# http://www.cs.ubbcluj.ro/~lauras/test/docs/school/IA/2019-2020/labs/lab03/lab03.pdf
# https://github.com/lauradiosan/AI-2019-2020/tree/master/lab03


if __name__ == '__main__':
    #convert1to2()
    #network = loadNet('net.in')
    network = loadNet('graphOnline.txt')
    plotRawNetwork(network['mat'])
    
    
    MIN = -1
    MAX = 1
    N = network['noNodes'] 
    fcEval = modularity
     
    seed(1)
    
    gaParam = {'popSize' : 10, 'noGen' : 5, 'pc' : 0.8, 'pm' : 0.1}
    problParam = {'min' : MIN, 'max' : MAX, 'function' : fcEval, 'noDim' : 1, 'vertices' : N, 'network': network}
    
    # store the best/average solution of each iteration (for a final plot used to anlyse the GA's convergence)
    allBestFitnesses = []
    allAvgFitnesses = []
    generations = []
    
    ga = GA(gaParam, problParam)
    ga.initialisation()
    ga.evaluation()
    
    bestRepres = None
    
    for g in range(gaParam['noGen']):
        #plotting preparation
        allPotentialSolutionsX = [c.repres for c in ga.population]
        allPotentialSolutionsY = [c.fitness for c in ga.population]
        bestSolX = ga.bestChromosome().repres
        bestSolY = ga.bestChromosome().fitness
        
        if bestRepres == None or bestSolY > modularity(detComunitati(bestRepres), network):
            bestRepres = bestSolX
        
        allBestFitnesses.append(bestSolY)
        allAvgFitnesses.append(sum(allPotentialSolutionsY) / len(allPotentialSolutionsY))
        generations.append(g)
        # plotAFunction(xref, yref, allPotentialSolutionsX, allPotentialSolutionsY, bestSolX, [bestSolY], 'generation: ' + str(g))
    
        #logic alg
        ga.oneGeneration()
        # ga.oneGenerationElitism()
        # ga.oneGenerationSteadyState()
        
        bestChromo = ga.bestChromosome()
        print('Best solution in generation ' + str(g) + ' is: x = ' + str(bestChromo.repres) + ' f(x) = ' + str(bestChromo.fitness))
    
    

    
    communities = detComunitati(bestRepres)
    print("BEST OVERALL ",communities)
    plotCommunities(communities, network)
    print(modularity(communities, network))




#    Homework
#    Add GA code for identifing the communities by using modularity as fitness function





