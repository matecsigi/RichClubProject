from igraph import *
from math import *
from random import *
import numpy
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import sys

seed()


def addToBridges(bridges, n):
    element = False
    for e in bridges:
        if e[0] == n:
            e[1] = e[1]+1
            return bridges
    bridges.append([])
    bridges[-1].append(n)
    bridges[-1].append(1)
    return bridges

def bridgeTest(G, fileObject):

    hubLimit = 50
    bridgeLimit = 1

    hubs = []
    for n in G.nodes():
        if G.degree(n) >= hubLimit:
            hubs.append(n)

    bridges = []
    for n in range(0, len(hubs)):
        for m in range(n+1, len(hubs)):
            path = nx.shortest_path(G, hubs[n], hubs[m])
            #print hubs[n], '->', hubs[m], ' = ', path
            for p in range(1, len(path)-1):
                bridges = addToBridges(bridges, path[p])

    finalBridges = []
    for b in bridges:
        if b[1] >= bridgeLimit:
            finalBridges.append([])
            finalBridges[-1].append(b[0])
            finalBridges[-1].append(b[1])

    fileObject.write("    Degree by analyzer program:\n    ")
    for i in finalBridges:
        #print i[0], ' -> ', G.degree(i[0])
        fileObject.write(" "+str(G.degree(i[0])))


def midpoint(radius1, angle1, radius2, angle2):
    # Compute the midpoint of two points
    x1 = radius1 * cos(angle1)
    x2 = radius2 * cos(angle2)
    y1 = radius1 * sin(angle1)
    y2 = radius2 * sin(angle2)
    xm, ym = (x1+x2)/2, (y1+y2)/2
    rm = sqrt(xm*xm+ym*ym)
    am = atan(ym/xm)
    return rm, am

def edist(radius1, angle1, radius2, angle2):
    # Compute euclidean distane
    x1 = radius1 * cos(angle1)
    x2 = radius2 * cos(angle2)
    y1 = radius1 * sin(angle1)
    y2 = radius2 * sin(angle2)
    return (sqrt(pow(x2-x1,2)+pow(y2-y1,2)))   

def erad(R):
    prob = random()
    return (sqrt(prob * R*R))

#--PARAMS------------------------------------
N = 500
R = 50                          # radius of disk
k = 3                           # number of connections when joining a node
limit = 12                       # if a link would be longer than this put a node into the midpoint
loopNumber = 15

fileName = "bridgeTime"+str(N)+"Rand"+str(randrange(1, 1000))+".txt"
fileObject = open(fileName, "w+")
#-----------------------

#----LOOP--------
bridgeTimeDict = {}
for i in range(0, N):
    bridgeTimeDict[i] = 0

#print "Our dict: ", bridgeTimeDict

for loop in range(0, loopNumber):
    g = Graph()

    # collect bridge nodes here
    bridge_nodes = []

    for nodes in range(0,N):
        bridgeTimeDict[nodes] = bridgeTimeDict[nodes]+len(bridge_nodes)
        curr_node = g.vcount()      # Nasty hacking with the labeling of the nodes (python indices start from zero)
        g.add_vertices(1)

        # Assign nodes with coordinates
        g.vs[curr_node]["radius"] = erad(R)
        g.vs[curr_node]["angle"] = uniform(0,2*pi)
        if curr_node==0: continue   # if this is the first node no edges needed
    
        dists = []
        ids = range(0,nodes)
        for node in range(0,nodes): # iterate through all existing nodes
            base_dist = edist(g.vs[curr_node]["radius"], g.vs[curr_node]["angle"], g.vs[node]["radius"],g.vs[node]["angle"])
            if curr_node < 2:
                eff_dist = base_dist
            else:
                eff_dist = base_dist / sqrt(g.degree()[node])
                
            # Use effective distance to produce scale-free graph (see Malkovs paper)
            dists.append(eff_dist)

        nodes_dists = numpy.sort(dists)[0:k] # Get the first k nodes with smallest length
        if numpy.max(nodes_dists) > limit:
            nodes_to_connect = numpy.argsort(dists)[0:k]
            for idx, val in enumerate(nodes_dists):
                if val > limit:     # If two nodest to connect are farther than limit put a middle node between them
                    g.add_vertices(1)
                    last_node = g.vcount()-1
                    bridge_nodes.append(last_node)
                    # Assign nodes with coordinates
                    r1 = g.vs[curr_node]["radius"]
                    a1 = g.vs[curr_node]["angle"]
                    r2 = g.vs[nodes_to_connect[idx]]["radius"]
                    a2 = g.vs[nodes_to_connect[idx]]["angle"]
                    g.vs[last_node]["radius"], g.vs[last_node]["angle"] = midpoint(r1, a1, r2, a2)
                    g.add_edges([(curr_node, last_node), (last_node, nodes_to_connect[idx])])
                    #g.add_edges([(curr_node, nodes_to_connect[idx])])
                else:
                    g.add_edges([(curr_node, nodes_to_connect[idx])])
            
        else:                       # If no edges are longer than limit just simply connect the node
            nodes_to_connect = numpy.argsort(dists)[0:k]
            edges_to_add=itertools.product(nodes_to_connect, [curr_node])
            elist = list(edges_to_add)
            g.add_edges(elist)


for i in range(0, N):
    bridgeTimeDict[i] = bridgeTimeDict[i]/float(loopNumber)
print "Final dict: ", bridgeTimeDict

fileObject.write("   Degree of bridge nodes:\n")
fileObject.write("x: \n"+str(bridgeTimeDict.keys()))
fileObject.write("y: \n"+str(bridgeTimeDict.values()))
plt.plot(bridgeTimeDict.keys(),bridgeTimeDict.values())
pdfName = "bridgeTime"+"rand"+str(randrange(1, 100))+".pdf"
plt.savefig(pdfName, format='pdf')
plt.close()


fileObject.close()
