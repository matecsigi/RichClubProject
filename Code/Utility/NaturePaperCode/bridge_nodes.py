from igraph import *
import networkx as nx
import matplotlib.pyplot as plt
import csv
import sys, getopt
import numpy


def globalBridges(g):

    bridgeness = [0]*(g.vcount())

    for src in range(0,10):
#    for src in range(0,g.vcount()):
        print(src)
        for dst in range(0,g.vcount()):
            paths = g.get_all_shortest_paths(src, dst)
            #print(paths)
            omega = len(paths)
            if omega==0:
                print("No path between %d and %d" % (src,dst))
                continue
            for node in range(0,g.vcount()):
                bri=0
                for path in paths:
                    if node in path:
                        ind = path.index(node)
                        if ind > 1 and ind < len(path)-2:
                            bri = bri + 1
                bridgeness[node] += bri/float(omega)

    #print(["%.2f" % v for v in bridgeness])
    #print(numpy.argsort(bridgeness)[-numberBridges:])
    return(numpy.argsort(bridgeness))

def globalBridgesFast(g):

    bridgeness = [0]*(g.vcount())

#    for src in range(0,10):
    for src in range(0,g.vcount()):
        print(src)
        paths = g.get_all_shortest_paths(src)
        #print(paths)
        dst = -1
        increments = [0]*(g.vcount())
        omega = 1
        for path in paths:
            this_dst = path[-1]
            if this_dst != dst:
                # New destination
                for i in range(0,g.vcount()):
                    bridgeness[i] += increments[i]/float(omega)
                increments = [0]*(g.vcount())
                omega=1
                dst = this_dst
            else:
                # Same destination
                omega += 1
            if len(path) < 4:
                continue
            for node in path[2:-2]:
                increments[node] += 1
            
    return(numpy.argsort(bridgeness))

def main(argv):

    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print 'Input file is', inputfile


    g = Graph.Read_GML(inputfile)

    finalBridges = globalBridgesFast(g)

    degreeList = g.degree(finalBridges)

    richfile=inputfile.split(".")[0] + "_bridge_degrees.txt"
    with open(richfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for index, value in enumerate(degreeList):
            writer.writerow([value])
                
    print("Number of bridges")
    print(len(finalBridges))


if __name__ == "__main__":
   main(sys.argv[1:])
