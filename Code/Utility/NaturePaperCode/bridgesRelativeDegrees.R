bridgenum <- 50
#k <- 1:500
k <- seq(0,1,0.001)

#Genfig

t100<-scan("5000_50_5_100_bridge_degrees.txt", what=list(degree=numeric(0)))
t12<-scan("5000_50_5_12_bridge_degrees.txt", what=list(degree=numeric(0)))

yt100 <- array()
yt12 <- array()

index <- 1
len100 <- length(t100$degree)
len12 <- length(t12$degree)

maxdeg <- max(t100$degree)
for (reldegree in k){
    j <- 0
    for (brdegree in t100$degree[(len100-bridgenum):len100]) {
        if (brdegree/maxdeg < reldegree) j <- j + 1
    }
    yt100[index] <- j
    index <- index + 1
}

index <- 1
maxdeg <- max(t12$degree)
for (reldegree in k){
    j <- 0
    for (brdegree in t12$degree[(len12-bridgenum):len12]) {
        if (brdegree/maxdeg < reldegree) j <- j + 1
    }
    yt12[index] <- j
    index <- index + 1
}

of="bridgeDegreeDistribution_generated.pdf"

pdf(file=of, height=7.5, width=8.2, paper='special')
par(mar=c(4.4,7.5,2,1))

plot(1, type="n",xlab="degree(k)", ylab="Number of bridges", xlim=c(0.01,0.7), ylim=c(1,bridgenum), cex.lab=2.8, cex.axis=2, log="")
box(lwd=1)

points(k,  yt100,col='green', pch=0, cex=1.5)
points(k,  yt12, col='blue', pch=1, cex=1.5)

legend("topright", legend = c("T=100",  "T=12"), pch=c(0, 1), col=c("green","blue"), inset=0.05, cex=2.6, bty="n",pt.cex=3)
dev.off()

#Realfig

scere<-scan("Scere20100614_bridge_degrees.txt", what=list(degree=numeric(0)))
gen<-scan("airport_bridge_degrees.txt", what=list(degree=numeric(0)))

yscere <- array()
ygen <- array()

lens <- length(scere$degree)
leng <- length(gen$degree)

index <- 1
maxdeg <- max(scere$degree)
for (reldegree in k){
    j <- 0
    for (brdegree in scere$degree[(lens-bridgenum):lens]) {
        if (brdegree/maxdeg < reldegree) j <- j + 1
    }
    yscere[index] <- j
    index <- index + 1
}

index <- 1
maxdeg <- max(gen$degree)
for (reldegree in k){
    j <- 0
    for (brdegree in gen$degree[(leng-bridgenum):leng]) {
        if (brdegree/maxdeg < reldegree) j <- j + 1
    }
    ygen[index] <- j
    index <- index + 1
}

of="bridgeDegreeDistribution_real.pdf"

pdf(file=of, height=7.5, width=8.2, paper='special')
par(mar=c(4.4,7.5,2,1))

plot(1, type="n",xlab="degree(k)", ylab="Number of bridges", xlim=c(0.01,1), ylim=c(1,bridgenum), cex.lab=2.8, cex.axis=2, log="")
box(lwd=1)

points(k,  yscere,col='blue', pch=0, cex=1.5)
points(k,  ygen, col='green', pch=1, cex=1.5)

legend("topright", legend = c("Airport",  "PPI"), pch=c(0, 1), col=c("green","blue"), inset=0.05, cex=2.6, bty="n",pt.cex=3)
dev.off()

