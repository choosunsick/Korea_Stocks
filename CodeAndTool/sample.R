library(quantmod)
library(xts)

read.file<-function(x){#x=파일이름
  path <- "../Korea_Stocks/Korea_Stocks_Full/"
  filename <- paste(path,x,".csv",sep = "")
  stockdata<-read.csv(file = filename,header =T,stringsAsFactors = F)
  colnames(stockdata)[1] <-"Date"
  stockdata <- stockdata[which(stockdata$Date =="2013-07-01"):which(stockdata$Date =="2018-07-31"),]
  stockdata <- as.xts(stockdata$Adj.Close,order.by=as.Date(stockdata$Date))
  stockdata <- monthlyReturn(stockdata)
  return(stockdata)
}
stock_list<-c("005490","066570","000660","035420","000720")

stock_data<- do.call(cbind,lapply(stock_list,FUN = function(i){read.file(i)}))
colnames(stock_data)<- stock_list

n <- 500
pvols<-c()
prets<-c()
weight_data <- matrix(0,n,NCOL(stock_data))
calculate<-function(x,n){#x=data
  mu<-matrix(colMeans(x[,1:NCOL(x)])*12,ncol = 1) 
  sigma<-as.matrix(cov(x[,1:NCOL(x)])*12) 
  inv_sigma<-as.matrix(solve(sigma))
  ivec<-rep(1,ncol(x[,1:NCOL(x)]))
  #Mu.p<-seq(0,max(mu)+0.05,length=n)
  Mu.p<-runif(n,min = 0,max = max(mu)+0.05)
  A<-matrix(c(t(mu)%*%inv_sigma%*%mu,t(ivec)%*%inv_sigma%*%mu,t(mu)%*%inv_sigma%*%ivec,t(ivec)%*%inv_sigma%*%ivec),2,2)
  for(i in 1:n){
    b<-matrix(c(Mu.p[i],1),ncol = 1)
    lambda <- solve(A,b)
    weight <-as.matrix(inv_sigma%*%(lambda[1]*mu+lambda[2]*ivec),ncol=1)
    weight_data[i,] <<- weight
    prets<-c(prets,t(weight)%*%mu)
    pvols<-c(pvols,sqrt(t(weight)%*%(sigma%*%weight)))
    ptemp<-data.frame(cbind(pvols,prets))
    ptemp$shape.ratio <- ptemp$pret/ptemp$pvol
  }
  return(ptemp)
}
ptemp<-calculate(stock_data,n)

p<-ggplot(data = ptemp,aes(x = pvols,y = prets))+geom_point(color="blue")+
  labs(x = "expected_volatility",y="expected_return")+theme(legend.position = "none")
p+annotate("text",x = c(ptemp$pvols[which.min(ptemp$pvols)],ptemp$pvols[which.max(ptemp$shape.ratio)]),
           y = c(ptemp$prets[which.min(ptemp$pvols)],ptemp$prets[which.max(ptemp$shape.ratio)])
           ,label=c("MVP","MSP"),col=c("black","red"))
          

#임의의 포트폴리오 집합
mu<-matrix(colMeans(stock_data[,1:NCOL(stock_data)])*12,ncol = 1) 
sigma<-as.matrix(cov(stock_data[,1:NCOL(stock_data)])*12) 

random_prets <- data.frame()
random_pvols <- data.frame()
for (i in 1:500) {
  rand_5<-runif(5)
  weights<- rand_5/sum(rand_5)
  weights<- as.matrix(weights)
  random_prets[i,1] <- sum(mu*weights)
  random_pvols[i,1] <- sqrt(t(weights)%*%(sigma%*%weights))
  p_random<-data.frame(random_prets,random_pvols)
  colnames(p_random) <- c("pret","pvol")
}
random_p<-ggplot(data = p_random,aes(x = pvol,y = pret))+geom_point(color="red")+
  labs(x = "expected_volatility",y="expected_return")+theme(legend.position = "none")
random_p
