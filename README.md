# 깃허브 설명

안녕하세요. LOPES팀의 추선식입니다. 저희 팀에서 주식과 관련된 프로젝트를 하면서 차트 분석을 비롯한 여러 가지 분석을 위한 주식 데이터가 필요하게 되었습니다. 이와 더불어 시중에서는 주식의 수치들을 눈으로 확인할 수 있지만, 직접적인 수치를 다루어 데이터를 만질 수 없기 때문에 주식 데이터를 직접 모으고 관리하려 합니다. [Yahoo Finance](https://finance.yahoo.com/)의 코스피, 코스닥 자료를 이용하여 한국 주식 자료를 수집하였습니다. 수집한 데이터들은 Korea_Stock_since_2018, Korea_Stock_Full 두 폴더에서 관리하는데 휴일을 제외하고 매일 갱신됩니다.

## 간단한 자료 소개

본 자료는 Yahoo Finance에서 한국 주식 데이터를 파이썬(Python)으로 크롤링하여 직접 수집한 것입니다. 크롤링에 필요한 파일들은 CodeAndTool 폴더에 있습니다. 파이썬 코드 파일을 터미널로 실행하면 자동으로 자료를 크롤링하고 전처리하여 저장합니다.

크롤링 된 주식 데이터는 temp 폴더에 저장됩니다. 이 자료들을 2018년 주식 데이터와 결합하여 저장한 파일들이 Korea_Stock_since_2018 폴더에 저장됩니다. Korea_Stock_Full 폴더에는 2018년 이전의 데이터와 지금까지의 데이터를 병합한 파일들이 저장됩니다.

## 자료에 대한 참고
주식들은 거래정지와 상장 폐지되는 경우가 있습니다. 거래정지는 주식 거래가 금지된 경우를 말합니다. 거래정지가 된 주식은 일정 기간 동안 거래가 없기에 데이터 또한 변화가 없습니다. 상장폐지의 경우 주식 거래가 종결되기 때문에 상장폐지가 결정된 날 이후로 해당 주식에 대한 데이터가 사라집니다. 이런 상황을 매일 체크해야 합니다. 따라서 현재[KRX 홈페이지](http://www.krx.co.kr/main/main.jsp)에서 [거래정지](http://marketdata.krx.co.kr/contents/MKD/04/0403/04030300/MKD04030300.jsp)와 [상장폐지](http://marketdata.krx.co.kr/contents/MKD/04/0406/04060600/MKD04060600.jsp) 목록을 확인할 수 있습니다. 확인된 목록을 total_stocklist.csv 파일에 당일의 상태열(col)로 만들고 있습니다. 이것은 해당 날짜에 크롤링할 주식 코드와 아닌 것을 구분하는 역할을 합니다.

야후의 서버 연결 문제는 코드가 실행되는 중에 가끔 야후와 서버 연결에 실패하여 주식 데이터가 크롤링 되지 않은 경우를 말합니다. 물론 코드 내에서 서버 에러가 난 주소들을 모아서 다시 한번 크롤링을 실행합니다. 그럼에도 불구하고 서버 에러가 나는 경우는 로그 파일(error_list.csv)로 저장됩니다. 이 파일을 가지고 해당 주식의 데이터를 수동으로 수집하거나 코드를 다시 한번 실행시키는 것으로 문제를 해결할 수 있습니다.
[github 이슈](https://github.com/choosunsick/Korea_Stocks/issues)를 통해 당일에 크롤링 되는 주식과 크롤링이 되지 않은 주식(거래정지와 상장 폐지된 것을 포함한 야후의 서버 에러로 크롤링에 실패한 목록)을 올릴 것입니다.

추가로 현재 자료 중 코스닥의 경우는 야후에서 과거 데이터를 저장하지 않기에 데이터가 없습니다. 따라서 일부 코스닥 데이터의 경우 불완전한 경우가 있습니다. Korea_Stock_since_2018 파일에 있는 주식 데이터 중 코스닥의 경우 3/7일의 데이터가 유실되어 없습니다. 예를 들어 주식 코드 152550, 099340, 099350, 096300, 168490 등의 경우 야후 파이낸스에 데이터가 나오지 않는 관계로 크롤링 되지 않습니다. 현재(2018-08-20) 298040은 야후 파이낸스에서 버그가 고쳐져 데이터가 나오게 됐습니다. Korea_Stock_Full 파일에서 주식 파일들의 2018년 이전 데이터는 인터넷을 통해 구한 것으로 [gomjellie의 깃허브](https://github.com/gomjellie/kospi-kosdaq-csv)사이트를 참고했습니다.

## 직접 주식 데이터를 받는 방법  

직접 주식 데이터를 다운 받고 싶은 경우에 다음과 같은 과정을 통해 자료를 다운로드할 수 있습니다. 기본적으로 파이썬 3.5 이상의 버전이 준비되어 있으면, 제 깃허브를 클론(cloan)하거나 다운받습니다. 다운이 완료됐을 경우 현재까지 주식 데이터 파일과 코드를 실행시키는데 필요한 것들이 들어옵니다.

전체 스크립트 코드 파일에서 파일이 저장되는 디렉토리 주소를 본인의 주소로 바꾸어 줍니다. 예를 들면 "/Users/choosunsick/Desktop/"가 붙어있는 코드를 모두 개인의 디렉토리(폴더) 주소로 바꾸어 줍니다. 이 코드들을 바꾸었다면 이제 준비는 끝났습니다. 주소가 변경되면 이제 당일의 주식시장이 마감된 시각인 4시 이후에 터미널을 작동하여 파이썬 스크립트 파일을 실행시키면 됩니다.

## 다운 받은 주식 자료를 활용하는 방법

자료를 통해 5개 주식의 포트폴리오 최적화와 단순 포트폴리오를 비교하는 것을 R 코드로 구현해보았습니다. 포트폴리오 최적화와 단순 포트폴리오 간의 비교로 포트폴리오를 구성하는 주식들의 최적 투자 비중을 알 수 있습니다. 즉 어떤 주식들에 대해 분산 투자할 떄 각 주식에 어떤 비중을 두고 투자해야 하는지를 파악할 수 있습니다.

예를 들면 5개 주식에 총 100만을 투자한다고 할 경우 금액을 나누는 비중은 다양한 경우가 나올 수 있습니다. 이때 포트폴리오 최적화를 할 경우 기대수익률과 위험성에 따라 각 주식에 대한 최적의 투자 비중을 정할 수 있습니다.

### 자료 읽어와서 수익률 구하기

먼저 5개 주식을 읽어옵니다. 저는 삼성전자, LG전자, SK하이닉스, 네이버, 현대건설을 선택해 자료를 읽었습니다. 포트폴리오를 구성하는 주식 데이터는 같은 기간을 뽑아 왔어도 거래 정지등의 이유로 자료의 숫자가 서로 다를 수 있습니다. 참고로 밑의 코드에서는 약 5년간의 일간 자료를 읽어옵니다. 데이터들의 숫자가 서로 다르기 때문에 월간형식으로 바꾸어줍니다. 단 월 기간으로 바꾸었음에도 데이터의 수가 서로 차이가 난다면 포트폴리오를 구성하는 종목을 바꿔야 합니다.  

```
install.packages("xts")
library(xts)
install.packages("quantmod")
library(quantmod)


read.file<-function(x){#x=파일이름
  path <- "/Users/choosunsick/Desktop/Korea_Stocks/Korea_Stocks_Full/"
  filename <- paste(path,x,".csv",sep = "")
  stockdata<-read.csv(file = filename,header =T,stringsAsFactors = F)
  colnames(stockdata)[1] <-"Date"
  stockdata <- stockdata[which(stockdata$Date =="2013-07-01"):which(stockdata$Date =="2018-07-31"),]
  stockdata <- as.xts(stockdata$Adj.Close,order.by=as.Date(stockdata$Date))
  stockdata <- monthlyReturn(stockdata)
  return(stockdata)
}

```
자료를 단순히 `read.csv`로 읽어도 되지만 여기서는 함수를 만들어서 사용했습니다. 함수를 만든 이유는 디렉토리 문제를 피해가기 위해서입니다. path 변수에 본인이 자료를 저장한 폴더의 절대주소를 넣어줌으로써 자료를 읽어오는 과정에서 디렉토리 문제를 피할 수 있습니다. 이제 함수에 필요한 주식 코드만 입력하면 자료를 바로 읽어올 수 있게 됩니다.

이 함수에서는 단순히 자료를 읽어오는 것과 함께 자료의 월율화가 이루어집니다. 월율화란 일간 자료를 월간 형식의 자료로 바꿔주는 것을 말합니다. 위 코드에서 일간 수정 종가자료를 월간 수익률의 형식으로 변화해 줍니다.

```
stock_list <- c("005930","066570","000660","035420","000720")
stock_data <- do.call(cbind,lapply(stock_list,FUN = function(i){read.file(i)}))
colnames(stock_data)<- stock_list

```
앞서 만든 `read.file()` 함수를 필요한 주식 코드별로 적용해 하나의 데이터로 만들어 줍니다. 데이터가 준비되었으니 투자 비중을 랜덤하게 적용해 투자 가능 집합들을 그려볼 수 있습니다.

```
install.packages("ggplot2")
library(ggplot2)

mu<-matrix(colMeans(stock_data[,1:NCOL(stock_data)])*12,ncol = 1)
sigma<-as.matrix(cov(stock_data[,1:NCOL(stock_data)])*12)

random_prets <- data.frame()
random_pvols <- data.frame()

for (i in 1:500) {
  rand_5<-runif(5)
  weights<- rand_5/sum(rand_5)
  weights<-as.matrix(weights)
  random_prets[i,1] <- sum(mu*weights)
  random_pvols[i,1] <- sqrt(t(weights)%*%(sigma%*%weights))
  p_random<-data.frame(random_prets,random_pvols)
  colnames(p_random) <- c("pret","pvol")
}
ggplot(data = p_random,aes(x = pvol,y = pret))+geom_point(color="red")+labs(x = "expected_volatility",y="expected_return")+theme(legend.position = "none")


```

포트폴리오의 평균 수익률과 공분산을 구해줍니다. 이것을 토대로 포트폴리오의 기대수익률과 분산의 계산을 반복해줍니다. 가중치는 0~1 사이의 임의의 소수점으로 정해집니다. 여기서 가중치가 각 주식에 대한 투자 비중이라 말할 수 있습니다. 구해진 기대 수익률(y)과 분산(x)의 집합들을 그리면 다음과 같이 나옵니다. 이 그림에서 가중치는 랜덤하게 정해지기 때문에 그릴 때 마다 점들의 위치가 달라질 수 있습니다.

![단순 투자기회 집합](https://user-images.githubusercontent.com/19144813/44575045-0d1a7100-a7c6-11e8-9268-cb7ce8534df2.jpeg)

```

n <- 500
pvols<-NULL
prets<-NULL
weight_data <- matrix(0,n,NCOL(stock_data))
calculate<-function(x,n){#x=data
  mu<-matrix(colMeans(x[,1:NCOL(x)])*12,ncol = 1)
  sigma<-as.matrix(cov(five_stock[,1:NCOL(x)])*12)
  inv_sigma<-as.matrix(solve(sigma))
  ivec<-rep(1,ncol(five_stock[,1:NCOL(x)]))
  Mu.p<-runif(n = n,min = 0,max = max(mu))
  A<-matrix(c(t(mu)%*%inv_sigma%*%mu,t(ivec)%*%inv_sigma%*%mu,t(mu)%*%inv_sigma%*%ivec,t(ivec)%*%inv_sigma%*%ivec),2,2)
  for(i in 1:n){
    b<-matrix(c(Mu.p[i],1),ncol = 1)
    lambda <- solve(A,b)
    weight <-as.matrix(inv_sigma%*%(lambda[1]*mu+lambda[2]*ivec),ncol=1)
    weight_data[i,] <<- weight
    prets<-c(prets,as.numeric(t(weight)%*%mu))
    pvols<-c(pvols,sqrt(as.numeric(t(weight)%*%sigma%*%weight)))
    ptemp<-data.frame(cbind(pvols,prets))
    ptemp$shape.ratio <- ptemp$pret/ptemp$pvol
  }
  return(ptemp)
}
ptemp<-calculate(stock_data,n)

```

```

p<-ggplot(data = ptemp,aes(x = pvols,y = prets))+geom_point(color="blue")+labs(x = "expected_volatility",y="expected_return")+theme(legend.position = "none")
p+annotate("text",x = ptemp$pvols[which.min(ptemp$pvols)],y = ptemp$prets[which.min(ptemp$pvols)],label="MVP")+annotate("text",x = ptemp$pvols[which.max(ptemp$shape.ratio)],y = ptemp$prets[which.max(ptemp$shape.ratio)],label="MSP")

```
이제 최적의 투자기회 집합 즉 효율적 투자선(efficient frontier)을 그려봅니다. 효율적 투자선은 같은 위험 수준 대비 최대 기대수익률 또는 같은 수익률 대비 최소 위험 수준을 가지는 투자 집합들을 말합니다. 이 그래프는 앞서 본 단순 투자기회 집합 그래프와 달리 특정한 형태를 보입니다. 그래프는 이차함수 곡선이 회전한 모습이지만, 실제로는 일정하게 배치된 점들이 연결되어 선처럼 보이는 것입니다. 그래프의 x, y 축은 단순 투자기회 집합의 그래프와 똑같이 x는 위험 수준을 나타내고 y는 포트폴리오의 기대수익률을 보여줍니다.

두 그래프는 x,y 축의 값과 모양에서 차이를 찾을 수 있습니다. 단순 투자기회 집합을 그렸을 때 위험 수준은 최대 0.35까지 될 수 있습니다. 반면 최적의 투자기회 집합은 위험 수준이 최대 0.22까지 밖에 나오지 않습니다. 즉 개별 주식에 대한 투자 비중을 어떻게 정하는가에 따라서 포트폴리오 전체의 위험 수준을 조절할 수 있습니다. 기대수익률 또한 마찬가지로 투자 비중에 따라 더 높은 기대수익률을 얻을 수 있습니다. 최적의 투자기회 집합 그래프에서 기대수익률의 최댓값은 0.25로 단순 투자기회 집합의 기대수익률의 최댓값인 0.20보다 높은 것을 확인할 수 있습니다.

최적의 투자기회 집합 그래프에서 주목할 점은 두 가지입니다. 바로 MVP점과 MSP점입니다. MVP는 최저 위험 수준일 때의 최대 기대수익률을 보여주는 점입니다. 이 점 위의 점들은 모두 특정한 위험 수준에 대한 최대 기대수익률을 나타내는 점입니다. 그중에서도 MSP는 최대 샤프지수일 때의 점을 의미합니다. [샤프지수(sharp.ratio)](https://ko.wikipedia.org/wiki/%EC%83%A4%ED%94%84_%EB%B9%84%EC%9C%A8)링크의 금융에서 용례를 살펴보면 샤프지수가 무엇인지 잘 알 수 있습니다. 물론 위 코드에서 샤프지수를 계산할 때 무위험 수익률을 편의를 위해 0으로 설정하여 계산했습니다. 따라서 MSP는 최대 기대수익률일 때 가장 낮은 위험 수준인 점을 의미합니다. 즉 이때의 투자 비중이 최대 기대수익률을 바랄 때 가장 낮은 위험 수준을 가진 최적의 투자 비중이라고 말할 수 있습니다.

![최적 투자기회 집합](https://user-images.githubusercontent.com/19144813/44575168-5c60a180-a7c6-11e8-8295-9ee89c24480a.jpeg)
