import sys
import networkx as nx
import igraph
import math
from mpmath import *
import random
import numpy
import matplotlib.pyplot as plt

def hyperbolicRadius(R):
    """Returns the radius corresponding to the parameter value."""
    alpha = 1
    curvature = -1
    prob = random.random()
    return acosh (prob * ((cosh ((-1 * curvature) * alpha * R)) - 1) + 1) / (-1 * curvature * alpha);

def hyperbolicDistance(G, node1, node2, beta=1):
    """Calculates the distance between two points in hyperbolic space."""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    r1 = G.node[node1]["radius"]
    r2 = G.node[node2]["radius"]
    delta = abs(angle1-angle2)
    #return abs(r1+r2+math.log(sin(delta/float(2))))
    dist = acosh(cosh(r1)*cosh(r2)-sinh(r1)*sinh(r2)*cos(delta))
    return dist.real

def addMiddleNode(G, node1, node2, id):
    """Add a new node between two nodes"""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    r1 = G.node[node1]["radius"]
    r2 = G.node[node2]["radius"]

    radiusesArray = numpy.linspace(float(r1), float(r2), num=10)
    if(abs(angle1-angle2) < math.pi):
        anglesArray =numpy.linspace(min(angle1, angle2), max(angle1, angle2), num=10)
    else:
        anglesArray = numpy.append(numpy.linspace(max(angle1,angle2), 2*math.pi, num=10), numpy.linspace(0, min(angle1,angle2), num=10))

    radiuses = radiusesArray.tolist()
    angles = anglesArray.tolist()
    
    fitnessMax = 0
    rMax = radiuses[0]
    angleMax = angles[0]
    for r in radiuses:
        for angle in angles:
            tmpG = G
            tmpG.add_node(id)
            tmpG.node[id]["radius"] = r
            tmpG.node[id]["angle"] = angle
            fitness = fitnessFunction(tmpG, id, node1, node2)
            if(fitness > fitnessMax):
                fitnessMax = fitness
                rMax = r
                angleMax = angle
    G.add_node(id)
    G.node[id]["radius"] = rMax
    G.node[id]["angle"] = angleMax

    # print "angle1=", angle1, " angle2=", angle2, " angle=", angleMax
    # print "radius1=", r1, " radius2=", r2, " radius=", rMax

def fitnessFunction(G, nodeMid, node1, node2):
    dist1 = hyperbolicDistance(G, node1, nodeMid)
    dist2 = hyperbolicDistance(G, nodeMid, node2)
    fitness = 10/(abs(dist1-dist2))+1/(dist1+dist2)
    return fitness
    
def addNode(G, id):
    """Adds a node to the network assigning coordinates to it."""
    G.add_node(id)
    G.node[id]["radius"] = radiuses[t]
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

def saveRichClub(G):
    try:
        rc = nx.rich_club_coefficient(G, normalized=True, Q=500)
        plt.plot(rc.keys(),rc.values())
        pdfName = "hyperbolicModel"+"N"+str(N)+"limit"+str(limitDistance)+"rand"+str(random.randrange(1, 100))+"_rich-club"+".pdf"
        plt.savefig(pdfName, format='pdf')
        plt.close()
    except:
        print "new try"
        saveRichClub(G)

def generateRadiuses(N, R):
    radiusList = []
    for i in range(0, N):
        radiusList.append(hyperbolicRadius(R))
    radiusList.sort()
    return radiusList

if __name__=='__main__':

    N = int(sys.argv[1])
    limitDistance = float(sys.argv[2])
    R = 16.5
    k = 3

    radiuses = generateRadiuses(N, R)

    G = nx.Graph()
    currentNodeID = 0

    for t in range(0, N):
        addNode(G, currentNodeID)

        midNodeID = currentNodeID
        for node in kClosest(G, currentNodeID, k):
            if hyperbolicDistance(G, currentNodeID, node) >= limitDistance:
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
    saveRichClub(G)
