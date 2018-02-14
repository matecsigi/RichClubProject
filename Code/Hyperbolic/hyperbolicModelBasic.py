import networkx as nx
import igraph
import math
import random
import numpy

def hyperbolicRadius(t):
    return math.log(t)

def hyperbolicDistance(radius1, angle1, radius2, angle2, beta=1):
    deltaAngle = abs(angle1-angle2)
    return radius1+radius2+math.log(deltaAngle/float(2))

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
        dists.append(hyperbolicDistance(G.node[nodeCounter]["radius"], G.node[nodeCounter]["angle"], G.node[nodesPresent]["radius"], G.node[nodesPresent]["angle"]))

    nodesToConnect = numpy.argsort(dists)[0:min(nodeCounter, k)]
    for node in nodesToConnect:
        G.add_edge(nodeCounter, node)
    
    nodeCounter += 1
        
g = igraph.Graph(directed=False)
g.add_vertices(G.nodes())
for node in G.nodes():
    g.vs[node]["radius"] = G.node[node]["radius"]
    g.vs[node]["angle"] = G.node[node]["angle"]
g.add_edges(G.edges())

g.save("orderedModel"+"rand"+str(random.randrange(1, 100))+".gml")
