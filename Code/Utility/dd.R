library(igraph)
library(graphics)
library(plotrix)
library(grid)
library(calibrate)

g_low <-read.graph("hyperbolicGraphN5000limit15loop0rand81.gml", format="gml")
num_vertices<-vcount(g_low)
ddlow<-degree.distribution(g_low,cumulative=FALSE,mode="total")
max_degree<-max(degree(g_low,mode="total"))

g_medium <-read.graph("hyperbolicGraphN5000limit20.0loop2rand19.gml", format="gml")
num_vertices<-vcount(g_medium)
ddmed<-degree.distribution(g_medium,cumulative=FALSE,mode="total")
max_degree<-max(degree(g_medium,mode="total"))

g_high <-read.graph("hyperbolicGraphN5000limit41.0loop0rand51.gml", format="gml")
num_vertices<-vcount(g_high)
ddhi<-degree.distribution(g_high,cumulative=FALSE,mode="total")
max_degree<-max(degree(g_high,mode="total"))


x_low<-array(0)
y_low<-array(0)

binsize <- 0.238
numbins<-log(3000,10^binsize)
bins<-array(0)
i<-0
currbin<-1
while (i < numbins){
	bins[i]<-currbin
	currbin<-currbin*10^binsize
	i<-i+1
}
counter<-1
vecc<-1
for (i in bins[1:(length(bins)-1)]) {
	if (ceiling(bins[counter])<ceiling(bins[counter+1])){
		x_low[vecc]<-(bins[counter]+bins[counter+1])/2
		y_low[vecc]<-sum(ddlow[ceiling(bins[counter]):ceiling(bins[counter+1])])/(ceiling(bins[counter+1])-ceiling(bins[counter]))
		vecc<-vecc+1
	}
	counter<-counter+1
}
print(bins)
print(sum(y_low,na.rm=TRUE))

x_medium<-array(0)
y_medium<-array(0)

binsize <- 0.2
numbins<-log(3000,10^binsize)
bins<-array(0)
i<-0
currbin<-1
while (i < numbins){
	bins[i]<-currbin
	currbin<-currbin*10^binsize
	i<-i+1
}
counter<-1
vecc<-1
for (i in bins[1:(length(bins)-1)]) {
	if (ceiling(bins[counter])<ceiling(bins[counter+1])){
		x_medium[vecc]<-i
		y_medium[vecc]<-sum(ddmed[ceiling(bins[counter]):ceiling(bins[counter+1])])/(ceiling(bins[counter+1])-ceiling(bins[counter]))
		vecc<-vecc+1
	}
	counter<-counter+1
}

print(bins)
print(sum(y_medium,na.rm=TRUE))

x_high<-array(0)
y_high<-array(0)

binsize <- 0.15
numbins<-log(1000,10^binsize)
bins<-array(0)
i<-0
currbin<-1
while (i < numbins){
	bins[i]<-currbin
	currbin<-currbin*10^binsize
	i<-i+1
}
counter<-1
vecc<-1
for (i in bins[1:(length(bins)-1)]) {
	if (ceiling(bins[counter])<ceiling(bins[counter+1])){
		x_high[vecc]<-i
		y_high[vecc]<-sum(ddhi[ceiling(bins[counter]):ceiling(bins[counter+1])])/(ceiling(bins[counter+1])-ceiling(bins[counter]))
		vecc<-vecc+1
	}
	counter<-counter+1
}

print(bins)
print(sum(y_high,na.rm=TRUE))

of="degreeDistFinal.pdf"
pdf(file=of, height=7.5, width=8.2, paper='special')
par(mar=c(4.4,7.5,2,1))
plot(1, type="n",xlab="Node degree", ylab="",xlim=c(1,1500),ylim=c(0.00000005,1),log="xy",cex.lab=2.8,axes=F)
title(ylab="Degree distribution",mgp=c(5.5,1,0),cex.lab=2.8)
axis(1,at=c(1,10,100,1000),label=c(expression(10^0),expression(10^1),expression(10^2),expression(10^3)),cex.axis=2.8)
axis(2,at=c(10^(0),10^(-1),10^(-2),10^(-3),10^(-4),10^(-5),10^(-6),10^(-7)),label=c(expression(10^0),expression(10^-1),expression(10^-2),expression(10^-3),expression(10^-4),expression(10^-5),expression(10^-6),expression(10^-7)),cex.axis=2.8,las=2)
box(lwd=1)
lines(x_low,y_low,lty=1,col="black",lw=3)
points(x_low,y_low,pch=22,col="black",cex=3,bg="blue",lwd=2)
lines(x_medium,y_medium,lty=1,col="black",lw=3)
points(x_medium,y_medium,pch=21,col="black",cex=3,,bg="green",lwd=2)
lines(x_high,y_high,lty=1,col="black",lw=3)
points(x_high,y_high,pch=24,col="black",cex=3,bg="red",lwd=2)

x<-1:5000
y<-(0.25*(x)^(-3.0))
lines(x,y,lty=2,col="black",lw=5)
text(7,0.00001,expression(y*"~"*x^-3.0),cex=2.6)
arrows(6,0.000015,10,0.00015,lwd=4)
legend("topright",inset=0.04, legend=c("T=100","T=30","T=12"),lty=c(1,1,1),pch=c(24,21,22),col=c("black","black","black"),pt.bg=c("red","green","blue"),bty="n",cex=2.6,pt.cex=3,lw=5)

dev.off()
