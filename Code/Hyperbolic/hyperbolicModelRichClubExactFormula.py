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

    angleDiff = max(angle1, angle2)-min(angle1, angle2)
    if angleDiff > math.pi:
        angleDiff = 2*math.pi-angleDiff

    angleMiddle = acot((sinh(r2)/sinh(r1))*(1/float(sin(angleDiff)))+cot(angleDiff))
    if angleMiddle < 0:
        angleMiddle = angleMiddle+math.pi

    #print "angle1=", angle1, " angle2=", angle2, " angleMiddle=", angleMiddle, " angleDiff=", angleDiff

    rMiddle = re(log(sqrt(-cosh(r1)+cosh(r2)-cos(angleMiddle-angleDiff)*sinh(r1)+cos(angleMiddle)*sinh(r2))/sqrt(cosh(r1)-cosh(r2)-cos(angleMiddle-angleDiff)*sinh(r1)+cos(angleMiddle)*sinh(r2))))

    if ((angle1 > angle2) and (angle1-angle2 < math.pi)) or ((angle2 > angle1) and (angle1-angle2 > math.pi)):
        angleMiddle = angle2-angleMiddle
    else:
        angleMiddle = angle2+angleMiddle

    if angleMiddle > 2*math.pi:
        angleMiddle = angleMiddle-2*math.pi

    if angleMiddle < 0:
        angleMiddle = angleMiddle+2*math.pi

    G.add_node(id)
    G.node[id]["radius"] = rMiddle
    G.node[id]["angle"] = angleMiddle

    #print "angle1=", angle1, " angle2=", angle2, " angle=", angleMiddle
    #print "radius1=", r1, " radius2=", r2, " radius=", rMiddle
    
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

    bridgeTime = {}
    bridgeTime[0] = 0

    for t in range(0, N):
        addNode(G, currentNodeID)

        bridgeTime[t+1] = bridgeTime[t]

        midNodeID = currentNodeID
        for node in kClosest(G, currentNodeID, k):
            if hyperbolicDistance(G, currentNodeID, node) >= limitDistance:
                midNodeID += 1
                addMiddleNode(G, currentNodeID, node, midNodeID)
                G.add_edge(currentNodeID, midNodeID)
                G.add_edge(midNodeID, node)

                bridgeTime[t+1] = bridgeTime[t+1]+1

                #dist1 = hyperbolicDistance(G, currentNodeID, midNodeID)
                #dist2 = hyperbolicDistance(G, midNodeID, node)
                #distSum = hyperbolicDistance(G, currentNodeID, node)
                #print dist1+dist2, "==", distSum

            else:
                G.add_edge(currentNodeID, node)

        currentNodeID = midNodeID+1
        
    print "nodes: ",len(G.nodes())
    print "edges: ", G.number_of_edges()
    # saveGML(G, N, limitDistance)
    # saveRichClub(G)

    print "bridgeTime=", bridgeTime.values()
