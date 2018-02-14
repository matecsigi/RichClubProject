#x<-c(100, 500, 1000, 2000, 5000)

#y<-c(2.555038, 3.532036, 4.046857, 4.151383, 4.518048)

x<-c(100, 500, 1000, 2000, 5000)

y<-c(5, 7, 9, 9, 10)

plot(x, y, pch=16, col="blue", ylim=c(4, 12), cex=2, xlab="Number of nodes",
ylab="Diameter", cex.axis=1.3, cex.lab=1.65)

legend("bottomright", legend = c("theory", "simulation"),
               lty = c(1, 0),pch=c(30, 16), col=c("darkblue", "blue"), inset=0.2, cex=1.5)


#points(x, fit, type="o", pch=15, col="blue")

d <- data.frame(x,y)  ## need to use data in a data.frame for predict()
logEstimate <- lm(y~log(x),data=d)

xvec <- seq(0,7000,length=101)
logpred <- predict(logEstimate,newdata=data.frame(x=xvec))
lines(xvec,logpred, col="darkblue", cex=2)
