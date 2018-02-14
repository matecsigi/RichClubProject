import sys
import networkx as nx
#import igraph
import math
import random
import numpy

def hyperbolicRadius(t):
    """Returns the radius corresponding to the parameter value."""
    return math.log(t)

def hyperbolicDistance(G, node1, node2, beta=1):
    """Calculates the distance between two points in hyperbolic space."""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    radius1 = G.node[node1]["radius"]
    radius2 = G.node[node2]["radius"]
    deltaAngle = abs(angle1-angle2)
    return abs(radius1+radius2+math.log(deltaAngle/float(2)))

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

#def saveGML(G):
#    """Saves the network in a gml format."""
#    g = igraph.Graph(directed=False)
#    g.add_vertices(G.nodes())
#    for node in G.nodes():
#        g.vs[node]["radius"] = G.node[node]["radius"]
#        g.vs[node]["angle"] = G.node[node]["angle"]
#        g.add_edges(G.edges())

#    g.save("orderedModel"+"rand"+str(random.randrange(1, 100))+".gml")

def wrong_addMiddleNode(G, node1, node2, id):
    """Adds a new node between to nodes."""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    radius1 = G.node[node1]["radius"]
    radius2 = G.node[node2]["radius"]
    fi = angle2-angle1
    fiMid = fi/(1+math.exp(radius1-radius2))
    radiusMid = 0.5*math.log((2*(1-math.cos(fi)))/((1-math.cos(fiMid))*(1-math.cos(fiMid))))
    G.add_node(id)
    G.node[id]["radius"] = radiusMid
    G.node[id]["angle"] = fiMid+angle1

def addMiddleNode(G, node1, node2, id):
    """Adds a new node between to nodes."""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    radius1 = G.node[node1]["radius"]
    radius2 = G.node[node2]["radius"]

    radiusDivision = 100
    angleDivision = 100

    deltaRadius = abs(radius2-radius1)
    referenceRadius = min(radius1, radius2)

    if abs(angle2-angle1) < math.pi:
        deltaAngle = abs(angle2-angle1)
        referenceAngle = min(angle1, angle2)
    else:
        referenceAngle = max(angle1, angle2)
        deltaAngle = 2*math.pi-abs(angle2-angle1)

    radius = numpy.linspace(0, deltaRadius, radiusDivision)
    angle = numpy.linspace(0, deltaAngle, angleDivision)

    G.add_node(id)
    G.node[id]["radius"] = radius[0]
    G.node[id]["angle"] = angle[0]

    minValue = 1000

    for iRad in radius[1:-1]:
        for iAng in angle[1:-1]:
            G.node[id]["radius"] = iRad+referenceRadius
            G.node[id]["angle"] = iAng+referenceAngle
            diffDist = abs(hyperbolicDistance(G, node1, id)-hyperbolicDistance(G, id, node2))
            onLine = hyperbolicDistance(G, node1, id)+hyperbolicDistance(G, id, node2)-hyperbolicDistance(G, node1, node2)
            if diffDist+onLine < minValue:
                minValue = diffDist+onLine
                minRad = iRad
                minAng = iAng
    G.node[id]["radius"] = minRad+referenceRadius
    G.node[id]["angle"] = minAng+referenceAngle
    print " +++", G.node[id]["radius"], "   ", G.node[id]["angle"] 
    #print minValue

if __name__=='__main__':

    N = int(sys.argv[1])
    limitDistance = float(sys.argv[2])
    k = 3

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

                dist1 = hyperbolicDistance(G, currentNodeID, midNodeID)
                dist2 = hyperbolicDistance(G, midNodeID, node)
                distSum = hyperbolicDistance(G, currentNodeID, node)
                print "--", dist1
                print "--", dist2
                print dist1+dist2, "==", distSum
            else:
                G.add_edge(currentNodeID, node)

        currentNodeID = midNodeID+1
        
    print len(G.nodes())
 #   saveGML(G)
