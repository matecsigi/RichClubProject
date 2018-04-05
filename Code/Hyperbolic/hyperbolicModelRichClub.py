import sys
import networkx as nx
import igraph
import math
from mpmath import *
import random
import numpy
import matplotlib.pyplot as plt

def hyperbolicRadius(t):
    """Returns the radius corresponding to the parameter value."""
    return math.log(t)

def hyperbolicDistance(G, node1, node2, beta=1):
    """Calculates the distance between two points in hyperbolic space."""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    r1 = G.node[node1]["radius"]
    r2 = G.node[node2]["radius"]
    delta = abs(angle1-angle2)
    #return abs(r1+r2+math.log(sin(delta/float(2))))
    return acosh(cosh(r1)*cosh(r2)-sinh(r1)*sinh(r2)*cos(delta))
    
def addNode(G, id):
    """Adds a node to the network assigning coordinates to it."""
    G.add_node(id)
    G.node[id]["radius"] = hyperbolicRadius(t+1)
    G.node[id]["angle"] = random.uniform(0, 2*math.pi)

def kClosest(G, id, k):
    """Returns a list of the k closest nodes of the given node."""
    dists = []
    for nodesPresent in range(0, id):
        dists.append(hyperbolicDistance(G, id, nodesPresent))
    return numpy.argsort(dists)[0:min(id, k)]

def saveGML(G, N, limit):
    """Saves the network in a gml format."""
    g = igraph.Graph(directed=False)
    g.add_vertices(G.nodes())
    for node in G.nodes():
        g.vs[node]["radius"] = G.node[node]["radius"]
        g.vs[node]["angle"] = G.node[node]["angle"]
    g.add_edges(G.edges())
    g.save("hyperbolicModel"+"N"+str(N)+"limit"+str(limit)+"rand"+str(random.randrange(1, 100))+".gml")

def addMiddleNode(G, node1, node2, id):
    """Add a new node between two nodes"""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    r1 = G.node[node1]["radius"]
    r2 = G.node[node2]["radius"]

    if angle1 > angle2:
        if angle1-angle2 < math.pi:
            delta = angle1-angle2
            reference = angle2
        else:
            delta = 2*math.pi-(angle1-angle2)
            reference = angle1
    else:
        if angle2-angle1 < math.pi:
            delta = angle2-angle1
            reference = angle1
        else:
            delta = 2*math.pi-(angle2-angle1)
            reference = angle2
    
    alpha = acot((sinh(r2)/sinh(r1))*(1/sinh(delta))+cot(delta))
    alpha = alpha.real
    if(alpha < 0):
        alpha = alpha+math.pi

    radius = log(sqrt(-cosh(r1)+cosh(r2)-cos(alpha-delta)*sinh(r1)+cos(alpha)*sinh(r2))/sqrt(cosh(r1)-cosh(r2)-cos(alpha-delta)*sinh(r1)+cos(alpha)*sinh(r2)))
    radius = radius.real

    G.add_node(id)
    G.node[id]["radius"] = radius
    if alpha+reference < 2*math.pi:
        G.node[id]["angle"] = alpha+reference
    else:
        G.node[id]["angle"] = alpha+reference-2*math.pi

def getLimitDistance(t):
    """Returns the current limit based on the current iteration"""
    #return math.log(t)*1.25
    if t < 30:
        return 5
    else:
        return 1000

if __name__=='__main__':

    N = int(sys.argv[1])
    limitDistance = float(sys.argv[2])
    k = 3

    G = nx.Graph()
    currentNodeID = 0

    for t in range(1, N):
        addNode(G, currentNodeID)
        
        midNodeID = currentNodeID
        for node in kClosest(G, currentNodeID, k):
            if hyperbolicDistance(G, currentNodeID, node) >= getLimitDistance(t):
                midNodeID += 1
                addMiddleNode(G, currentNodeID, node, midNodeID)
                G.add_edge(currentNodeID, midNodeID)
                G.add_edge(midNodeID, node)

                #dist1 = hyperbolicDistance(G, currentNodeID, midNodeID)
                #dist2 = hyperbolicDistance(G, midNodeID, node)
                #distSum = hyperbolicDistance(G, currentNodeID, node)
                #print dist1+dist2, "==", distSum

            else:
                G.add_edge(currentNodeID, node)

        currentNodeID = midNodeID+1
        
    print "nodes: ",len(G.nodes())
    print "edges: ", G.number_of_edges()
    saveGML(G, N, limitDistance)

    for i in range(0,10):
        rc = nx.rich_club_coefficient(G, normalized=True, Q=500)
        plt.plot(rc.keys(),rc.values())
        pdfName = "hyperbolicModel"+"N"+str(N)+"limit"+str(limitDistance)+"rand"+str(random.randrange(1, 100))+"_rich-club"+".pdf"
        plt.savefig(pdfName, format='pdf')
        plt.close()
