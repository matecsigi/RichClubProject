import sys
import networkx as nx
import igraph
import math
import random
import numpy
from mpmath import *

def hyperbolicRadius(t):
    return math.log(t)

def hyperbolicDistance(G, node1, node2, beta=1):
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    r1 = G.node[node1]["radius"]
    r2 = G.node[node2]["radius"]
    deltaAngle = abs(angle1-angle2)
    if(deltaAngle > math.pi):
        deltaAngle = 2*math.pi-deltaAngle
    return r1+r2+math.log(deltaAngle/float(2))

def hyperbolicDistance2(G, node1, node2, beta=1):
    """Calculates the distance between two points in hyperbolic space."""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    r1 = G.node[node1]["radius"]
    r2 = G.node[node2]["radius"]
    delta = abs(angle1-angle2)
    #return abs(r1+r2+math.log(sin(delta/float(2))))
    return acosh(cosh(r1)*cosh(r2)-sinh(r1)*sinh(r2)*cos(delta))

def saveGML(G, N):
    """Saves the network in a gml format."""
    g = igraph.Graph(directed=False)
    g.add_vertices(G.nodes())
    for node in G.nodes():
        g.vs[node]["radius"] = G.node[node]["radius"]
        g.vs[node]["angle"] = G.node[node]["angle"]
    g.add_edges(G.edges())
    g.save("hyperbolicModelBasic"+"N"+str(N)+"rand"+str(random.randrange(1, 100))+".gml")

N = int(sys.argv[1])
k = 3

G = nx.Graph()
nodeCounter = 0
for t in range(1, N):
    G.add_node(nodeCounter)
    G.node[nodeCounter]["radius"] = hyperbolicRadius(t)
    G.node[nodeCounter]["angle"] = random.uniform(0, 2*math.pi)

    dists = []
    for nodesPresent in range(0, nodeCounter):
        dists.append(hyperbolicDistance2(G, nodeCounter, nodesPresent))

    nodesToConnect = numpy.argsort(dists)[0:min(nodeCounter, k)]
    for node in nodesToConnect:
        G.add_edge(nodeCounter, node)
    
    nodeCounter += 1

saveGML(G, N)
