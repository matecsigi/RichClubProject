 
#scere<-scan("Scere20100614_bridge_degrees.txt", what=list(degree=numeric(0)))
#gen<-scan("5000_50_5_12_bridge_degrees.txt", what=list(degree=numeric(0)))

scere<-scan("Scere20100614_bridge_degrees.txt", what=list(degree=numeric(0)))
gen<-scan("airport_bridge_degrees.txt", what=list(degree=numeric(0)))


#scere<-scan("test_bridge_degrees100.txt", what=list(degree=numeric(0)))
#gen<-scan("test_bridge_degrees12.txt", what=list(degree=numeric(0)))


k <- 1:1500

yscere <- array()
ygen <- array()

for (degree in k){
    j <- 0
    for (brdegree in scere$degree) {
        if (brdegree > degree) j <- j + 1
    }
    yscere[degree] <- j/length(scere$degree)
}

for (degree in k){
    j <- 0
    for (brdegree in gen$degree) {
        if (brdegree > degree) j <- j + 1
    }
    ygen[degree] <- j/length(gen$degree)
}

of="bridgeDegreeDistribution.pdf"

pdf(file=of, height=7.5, width=8.2, paper='special')
par(mar=c(4.4,7.5,2,1))

plot(1, type="n",xlab="degree(k)", ylab="F(k)", xlim=c(1, length(k)), ylim=c(0.02,1.0), cex.lab=2.8, cex.axis=2, log="xy")
box(lwd=1)

points(k,  yscere,col='blue', pch=0, cex=1.5)
points(k,  ygen, col='green', pch=1, cex=1.5)

legend("topright", legend = c("PPI",  "T=12"), pch=c(2, 1), col=c("blue","green"), inset=0.05, cex=2.6, bty="n",pt.cex=3)
dev.off()
