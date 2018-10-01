 
from igraph import *
from igraph import *
from math import *
from random import *
import numpy
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import sys
import csv

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

def bridgeTest(g, bridge_nodes):

    bridgeness = [0]*(g.vcount())

    for src in range(0,g.vcount()):
        print(src)
        for dst in range(0,g.vcount()):
            paths = g.get_all_shortest_paths(src, dst)
            #print(paths)
            omega = len(paths)
            for node in range(0,g.vcount()):
                bri=0
                for path in paths:
                    if node in path:
                        ind = path.index(node)
                        if ind > 1 and ind < len(path)-2:
                            bri = bri + 1
                bridgeness[node] += bri/float(omega)

    print(["%.2f" % v for v in bridgeness])
    print(bridge_nodes)
    print([bridgeness[i] for i in  bridge_nodes])
    print(numpy.argsort(bridgeness)[-50:])
    print(set(bridge_nodes).intersection(numpy.argsort(bridgeness)[-len(bridge_nodes):]))
    return(g.degree(numpy.argsort(bridgeness)[-50:]))
    
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

print "frist parameter number of nodes (N), second step interval:"

N = 1000
intervalStep = 1

print "N="+str(N)+" intervalStep="+str(intervalStep)

R = 50                         # radius of disk
k = 5                           # number of connections when joining a node

downerLimit = 12
upperLimit = 12
numberOfLoopsPerValue = 1

fileName = "bridgeDegree"+str(N)+"Rand"+str(randrange(1, 1000))+".txt"
fileObject = open(fileName, "w+")
fileObject.write("Homophilic model\n N="+str(N)+", downerLimit="+str(downerLimit)+" upperLimit="+str(upperLimit))

#----LOOP--------
intervalCounter = downerLimit
while intervalCounter <= upperLimit:
    limit = intervalCounter
    print "limit=", limit
    for loop in range(0, numberOfLoopsPerValue):
        g = Graph()
        
        fileObject.write("LIMIT="+str(limit)+" LOOP="+str(loop))

        # collect bridge nodes here
        bridge_nodes = []

        for node in range(0,k+1):
            curr_node = g.vcount()      # Nasty hacking with the labeling (python indices start from zero)
            g.add_vertices(1)
            # Assign nodes with coordinates
            g.vs[curr_node]["radius"] = erad(R)
            g.vs[curr_node]["angle"] = uniform(0,2*pi)

        for src in range(0,k):
            for dst in range(src+1,k+1):
                if src!=dst:
                    base_dist = edist(g.vs[src]["radius"], g.vs[src]["angle"], g.vs[dst]["radius"],g.vs[dst]["angle"])
                    if base_dist > limit:
                        g.add_vertices(1)
                        last_node = g.vcount()-1
                        bridge_nodes.append(last_node)
                        # Assign nodes with coordinates
                        r1 = g.vs[src]["radius"]
                        a1 = g.vs[src]["angle"]
                        r2 = g.vs[dst]["radius"]
                        a2 = g.vs[dst]["angle"]
                        g.vs[last_node]["radius"], g.vs[last_node]["angle"] = midpoint(r1, a1, r2, a2)
                        g.add_edges([(src, last_node), (last_node, dst)])
                    else:
                        g.add_edges([(src,dst)])
                        
        for nodes in range(g.vcount(),N+g.vcount()):
            curr_node = g.vcount()      # Nasty hacking with the labeling of the nodes (python indices start from zero)
            g.add_vertices(1)
#            print(curr_node)
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
                    else:
                        g.add_edges([(curr_node, nodes_to_connect[idx])])
            
            else:                       # If no edges are longer than limit just simply connect the node
                nodes_to_connect = numpy.argsort(dists)[0:k]
                edges_to_add=itertools.product(nodes_to_connect, [curr_node])
                elist = list(edges_to_add)
                g.add_edges(elist)

        fileObject.write("   Degree of bridge nodes:\n    "+str(g.degree(bridge_nodes))+"\n")
        
        A = g.get_edgelist()
        #itt a networkx graph
        G = nx.Graph(A)

        fileObject.write("\n\n")
        rc = nx.rich_club_coefficient(G,normalized=True,Q=1000)
        fileObject.write("x: \n"+str(rc.keys()))
        fileObject.write("y: \n"+str(rc.values()))
        plt.plot(rc.keys(),rc.values())
        pdfName = "rich"+str(intervalCounter)+"loop"+str(loop)+"rand"+str(randrange(1, 100))+".pdf"
        plt.savefig(pdfName, format='pdf')
        plt.close()

        print(g.vcount())
        global_bridge_degree = bridgeTest(g, bridge_nodes)

        outfile="test_bridge_degrees12.txt"
        with open(outfile, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for index, value in enumerate(global_bridge_degree):
                writer.writerow([value])
        
    intervalCounter = intervalCounter+intervalStep
    print(max(g.degree()))

fileObject.close()
