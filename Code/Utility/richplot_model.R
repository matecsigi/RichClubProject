 
data1<-scan("5000_50_3_12_rich.txt", what=list(degree=numeric(0),richcoeff=numeric(0)))
data2<-scan("5000_50_3_30_rich.txt", what=list(degree=numeric(0),richcoeff=numeric(0)))
data3<-scan("5000_50_3_100_rich.txt", what=list(degree=numeric(0),richcoeff=numeric(0)))
#data$degree <- as.numeric(data$degree)
#data$radius <- as.numeric(data$radius)
x1 <-data1$degree 
y1 <-data1$richcoeff 
x2 <-data2$degree 
y2 <-data2$richcoeff 
x3 <-data3$degree 
y3 <-data3$richcoeff 

of="generatedRichFinal.pdf"

pdf(file=of, height=7.5, width=8.2, paper='special')
par(mar=c(4.4,7.5,2,1))

plot(1, type="n",xlab="degree(k)", ylab=expression(rho(k)), xlim=c(0, 150), ylim=c(0.3,1.5), cex.lab=2.8, cex.axis=2)
box(lwd=1)
points(x1[seq(1, length(x1), 1)],  y1[seq(1, length(y1), 1)],col='blue', pch=0, cex=1.5)
points(x2[seq(1, length(x2), 1)],  y2[seq(1, length(y2), 1)], col='green', pch=1, cex=1.5)
points(x3[seq(1, length(x3), 1)],  y3[seq(1, length(y3), 1)], col='red', pch=2, cex=1.5)
legend("topleft", legend = c("T=100",  "T=30", "T=12"), pch=c(2, 1, 0), col=c("red", "green","blue"), inset=0.05, cex=2.6, bty="n",pt.cex=3)
dev.off()
