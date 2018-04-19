library(igraph)

#Usage from command line: Rscript gml_plotter.R --args test.gml model

options(warn=-1)

cmd_args = commandArgs();

infile<-cmd_args[7]
model<-cmd_args[8]

print(infile)

g<-read.graph(infile,format="gml")

if (model == "euclidean") {
	print("euc")
	#generate layout from gml file
	num_vertices<-vcount(g)
	glay <- matrix(0, nrow = num_vertices, ncol=2,byrow=TRUE)

	for (sw in V(g)){
		glay[sw,1]<-V(g)[sw]$radius * cos(V(g)[sw]$angle)
		glay[sw,2]<-V(g)[sw]$radius * sin(V(g)[sw]$angle)
	}
}

if (model == "hyperbolic") {
	print("hyp")
	#generate layout from gml file
	num_vertices<-vcount(g)
	glay <- matrix(0, nrow = num_vertices, ncol=2,byrow=TRUE)

	for (sw in V(g)){
		glay[sw,1]<-V(g)[sw]$radius * cos(V(g)[sw]$angle)
		glay[sw,2]<-V(g)[sw]$radius * sin(V(g)[sw]$angle)
	}

#        print(glay)
}

if (model == "poincare") {
	print("poin")
	#generate layout from gml file
	num_vertices<-vcount(g)
	glay <- matrix(0, nrow = num_vertices, ncol=2,byrow=TRUE)

	for (sw in V(g)){
		glay[sw,1]<-V(g)[sw]$x
		glay[sw,2]<-V(g)[sw]$y
	}
}


if (model == "spherical") {
	print("sph")
	#generate layout from gml file
	num_vertices<-vcount(g)
	glay <- matrix(0, nrow = num_vertices, ncol=2,byrow=TRUE)
	rho<-1

	for (sw in V(g)){
		glay[sw,1]<-rho * sin(V(g)[sw]$radius/rho) * cos(V(g)[sw]$angle)
		glay[sw,2]<-rho * sin(V(g)[sw]$radius/rho) * sin(V(g)[sw]$angle)
	}
}



#To be a bit more fancy and visible

V(g)$color="blue"
V(g)$size=1
E(g)$color="lightblue"
E(g)$width=0.5

#of="graph_plot.ps"
of<-paste(strsplit(infile,"\\.")[[1]][1],"ps",sep=".")
postscript(of,width=7.0,height=7.0,paper = "special", horizontal = FALSE)
plot(g,layout=glay,vertex.label.family="Helvetica", vertex.label.cex=0.6,vertex.label="",vertex.size=1,edge.arrow.size=0.2)
## # plot(g,layout=glay,vertex.label.family="Helvetica", vertex.label.cex=1,vertex.label=V(g)$id,vertex.size=1,edge.arrow.size=0.2)
points(0,0) 
dev.off()


#degree distribution
of<-paste(strsplit(infile,"\\.")[[1]][1],"in_deg.ps",sep="_")
postscript(of,width=7.0,height=7.0,paper = "special", horizontal = FALSE)
#In case we are interested in the undirected case
#g<-as.undirected(g, mode="collapse") 
#dd<-degree.distribution(g,cumulative=TRUE,mode="out")
#max_degree<-max(degree(g,mode="out"))
 dd<-degree.distribution(g,cumulative=TRUE,mode="in")
 max_degree<-max(degree(g,mode="in"))
#dd<-degree.distribution(g,cumulative=TRUE,mode="total")
#max_degree<-max(degree(g,mode="total"))
plot(0:max_degree,dd,xlab="Degree",ylab="Frequency", log="xy",main="The cumulative in degree distribution in a log-log scale")
coef<-coef(lm (log10(dd) ~ log10(1:(max_degree+1))))
pl_est<- -coef[2]
#lines(((1:(max_degree+1))^(coef[2])) * 10^(coef[1]))
lines(((1:(max_degree+1))^(-2)) * 10^(coef[1]))
dev.off()

#degree distribution
of<-paste(strsplit(infile,"\\.")[[1]][1],"out_deg.ps",sep="_")
postscript(of,width=7.0,height=7.0,paper = "special", horizontal = FALSE)
#In case we are interested in the undirected case
#g<-as.undirected(g, mode="collapse") 
#dd<-degree.distribution(g,cumulative=TRUE,mode="out")
#max_degree<-max(degree(g,mode="out"))
 dd<-degree.distribution(g,cumulative=TRUE,mode="out")
 max_degree<-max(degree(g,mode="out"))
#dd<-degree.distribution(g,cumulative=TRUE,mode="total")
#max_degree<-max(degree(g,mode="total"))
plot(0:max_degree,dd,xlab="Degree",ylab="Frequency", log="xy",main="The cumulative out degree distribution in a log-log scale")
coef<-coef(lm (log10(dd) ~ log10(1:(max_degree+1))))
pl_est<- -coef[2]
#slope -2
#lines(((1:(max_degree+1))^(-2)) * 10^(coef[1]))

#for greedy frame
#lines(0.1715267*(1:(max_degree+1))^(-1.1))
lines(0.29245*(1:(max_degree+1))^(-1.5))
dev.off()

#degree distribution
of<-paste(strsplit(infile,"\\.")[[1]][1],"total_deg.ps",sep="_")
postscript(of,width=7.0,height=7.0,paper = "special", horizontal = FALSE)
#In case we are interested in the undirected case
#g<-as.undirected(g, mode="collapse") 
#dd<-degree.distribution(g,cumulative=TRUE,mode="out")
#max_degree<-max(degree(g,mode="out"))
# dd<-degree.distribution(g,cumulative=TRUE,mode="out")
# max_degree<-max(degree(g,mode="out"))
dd<-degree.distribution(g,cumulative=TRUE,mode="total")
max_degree<-max(degree(g,mode="total"))
plot(0:max_degree,dd,xlab="Degree",ylab="Frequency", log="xy",main="The cumulative out degree distribution in a log-log scale")
coef<-coef(lm (log10(dd) ~ log10(1:(max_degree+1))))
pl_est<- -coef[2]
#lines(((1:(max_degree+1))^(coef[2])) * 10^(coef[1]))
lines(((1:(max_degree+1))^(-2)) * 10^(coef[1]))
dev.off()


avg_degree_in <- mean(degree(g,mode="in"))
avg_degree_out <- mean(degree(g,mode="out"))


#g<-as.undirected(g,mode="collapse")
of<-paste(strsplit(infile,"\\.")[[1]][1],"txt",sep=".")
cat("", file=of, append=FALSE)
avgdist<-average.path.length(g, directed=FALSE, unconnected=TRUE)
#avgdist<-average.path.length(g, directed=TRUE, unconnected=FALSE)
diam<-diameter(g, directed=FALSE, unconnected=TRUE)
#diam<-diameter(g, directed=TRUE, unconnected=FALSE)
max_cluster<-max(clusters(g)$csize)
#t<-transitivity(g,type="global")
t<-mean(transitivity(g,type="local")[which(degree(g)>1)])
cat("vcount", vcount(g), "\tecount", ecount(g), "\tavgdeg\t", (ecount(g)*2)/vcount(g), "\tavgdeg_in\t", avg_degree_in, "\tavgdeg_out\t", avg_degree_out, "\tavgdist\t", avgdist, "\tdiameter\t", diam, "\tmax_cluster_size\t", max_cluster, "\tmax_degree\t", max_degree,"\tclustering\t", t,"\n", file=of, append=TRUE)
cat("vcount", vcount(g), "\tecount", ecount(g), "\tavgdeg\t", (ecount(g)*2)/vcount(g),  "\tavgdeg_in\t", avg_degree_in, "\tavgdeg_out\t", avg_degree_out, "\tavgdist\t", avgdist, "\tdiameter\t", diam, "\tmax_cluster_size\t", max_cluster, "\tmax_degree\t", max_degree,"\tclustering\t", t,"\n")
