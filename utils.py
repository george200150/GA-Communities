'''
Created on 14 mar. 2020

@author: George
'''

from random import uniform, randint
import os
from copy import deepcopy

def generateNewValue(lim1, lim2):
    return int(round(uniform(lim1, lim2)))

def binToInt(x):
    val = 0
    # x.reverse()
    for bit in x:
        val = val * 2 + bit
    return val

def findNot999(repres):
    for i in range(0,len(repres)):
        if repres[i] != -999:
            return i
    return None

def toSet(bag):
    theSet = []
    for elem in bag:
        if elem not in theSet:
            theSet.append(elem)
    return theSet

"""def comparator(a, b):
    if a == None:
        return True
    elif b == None:
        return False
    elif a > b:
        return True
    else:
        return False """

def detCompConexe(representants): # determinat componentele conexe formate din inlantuirea vecinilor (?cred?)
    clusters = []
    repres = deepcopy(representants) # not necessary
    
    while True:
        first999 = findNot999(repres)
        if first999 == None:
            break
        cluster1 = []
        cluster1.append(first999)
        cluster1.append(repres[first999])
        repres[first999] = -999
        for i in range(0,len(repres)):
            if repres[i] != -999 and (repres[i] in cluster1 or i in cluster1):
                cluster1.append(i)
                cluster1.append(repres[i])
                repres[i] = -999
            
        clusters.append(toSet(cluster1)) #, key=comparator # add the unique (maybe sorted) vertices to the cluster
    return clusters

def detComunitati(repres):
    N = len(repres)
    compConexe = detCompConexe(repres)
    
    communities = [-1 for _ in range(0, N)]
    kCluster = 0
    
    for conex in compConexe:
        for vertex in conex:
            if vertex != None:
                if communities[vertex] == -1:
                    communities[vertex] = kCluster
                else: # overwrite (with a 50-50 probability)
                    p = generateNewValue(0, 1)
                    if p == 0:
                        communities[vertex] = kCluster
                    else:
                        pass # ramane asa
        kCluster += 1
    
    return communities



# read the network details
def __readNet(fileName):
    f = open(fileName, "r")
    net = {}
    n = int(f.readline())
    net['noNodes'] = n
    mat = []
    for i in range(n):
        mat.append([])
        line = f.readline()
        elems = line.split(" ")
        for j in range(n):
            mat[-1].append(int(elems[j]))
    net["mat"] = mat 
    degrees = []
    noEdges = 0
    for i in range(n):
        d = 0
        for j in range(n):
            if (mat[i][j] == 1):
                d += 1
            if (j > i):
                noEdges += mat[i][j]
        degrees.append(d)
    net["noEdges"] = noEdges
    net["degrees"] = degrees
    f.close()
    return net





# load a network
def loadNet(path):
    crtDir =  os.getcwd()
    filePath = os.path.join(crtDir, path) # 'net.in'
    network = __readNet(filePath)
    return network



