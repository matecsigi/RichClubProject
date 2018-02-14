library(igraph)

g_low <-read.graph("hyperbolicGraphN5000limit15loop0rand81.gml", format="gml")

g_medium <-read.graph("hyperbolicGraphN5000limit20.0loop2rand19.gml", format="gml")

g_high <-read.graph("hyperbolicGraphN5000limit41.0loop0rand51.gml", format="gml")

#air <-read.graph("airport.gml", format="gml")
#as <-read.graph("asgraph.gml", format="gml")
#ppi <-read.graph("Scere20130131.gml", format="gml")

assortativity_degree(g_low, directed = FALSE)
assortativity_degree(g_medium, directed = FALSE)
assortativity_degree(g_high, directed = FALSE)
#assortativity_degree(air, directed = FALSE)
#assortativity_degree(as, directed = FALSE)
#assortativity_degree(ppi, directed = FALSE)
