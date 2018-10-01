library(igraph)



edist <- function(radius1, angle1, radius2, angle2){
    # Compute euclidean distane
    x1 = radius1 * cos(angle1)
    x2 = radius2 * cos(angle2)
    y1 = radius1 * sin(angle1)
    y2 = radius2 * sin(angle2)
    return (sqrt((x2-x1)^2+(y2-y1)^2))   
}

g12 <- read.graph("5000_50_5_12.gml", format="gml")
g20 <- read.graph("5000_50_5_20.gml", format="gml")
g100 <- read.graph("5000_50_5_100.gml", format="gml")


of="edgeDistribution.pdf"

pdf(file=of, height=7.5, width=8.2, paper='special')
par(mar=c(4.4,7.5,2,1))

plot(1, type="n",xlab="edge length", ylab="ECDF", xlim=c(1, 100), ylim=c(0.01,1), cex.lab=2.8, cex.axis=2)
box(lwd=1)

qx <- seq(0,1,0.01)
lqx <- length(qx)

dists <- array(0)
limit <- 50000
index <- 0
for (edge in E(g12)){
#for (edge in E(g12)[0:100]){
    src <- ends(g12, edge)[[1]]
    dst <- ends(g12, edge)[[2]]
    dist <- edist(V(g12)[src]$radius, V(g12)[src]$angle, V(g12)[dst]$radius, V(g12)[dst]$angle)
    dists <- append(dists,dist)
    if (index%%1000 == 0) {print(index)}
    index <- index + 1
    if (index>limit) break
}

#lines(ecdf(dists),col="blue", lwd=3)
qy <- quantile(dists,qx)
lines(qy,qx,col="blue", lwd=3)

dists <- array(0)
index <- 0
for (edge in E(g20)){
    src <- ends(g20, edge)[[1]]
    dst <- ends(g20, edge)[[2]]
    dist <- edist(V(g20)[src]$radius, V(g20)[src]$angle, V(g20)[dst]$radius, V(g20)[dst]$angle)
    dists <- append(dists,dist)
    if (index%%1000 == 0) {print(index)}
    index <- index + 1
    if (index>limit) break
}

#lines(ecdf(dists),col="green",lwd=3)
qy <- quantile(dists,qx)
lines(qy,qx,col="green", lwd=3)

dists <- array(0)
index <- 0
for (edge in E(g100)){
    src <- ends(g100, edge)[[1]]
    dst <- ends(g100, edge)[[2]]
    dist <- edist(V(g100)[src]$radius, V(g100)[src]$angle, V(g100)[dst]$radius, V(g100)[dst]$angle)
    dists <- append(dists,dist)
    if (index%%1000 == 0) {print(index)}
    index <- index + 1
    if (index>limit) break
}

#lines(ecdf(dists), col="red",lwd=3)
qy <- quantile(dists,qx)
lines(qy,qx,col="red", lwd=3)


legend("bottomright", legend = c("T=100",  "T=20", "T=12"), col=c("red", "green","blue"), inset=0.05, cex=2.6, bty="n",pt.cex=3, lwd=c(3,3,3))
dev.off()

