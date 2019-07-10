# 깃허브 설명

안녕하세요. LOPES팀의 추선식입니다. 저희 팀에서 주식과 관련된 프로젝트를 하면서 차트 분석을 비롯한 여러 가지 분석을 위한 주식 데이터가 필요하게 되었습니다. 이와 더불어 시중에서는 주식의 수치들을 눈으로 확인할 수 있지만, 직접적인 수치를 다루어 데이터를 만질 수 없기 때문에 주식 데이터를 직접 모으고 관리하려 합니다. [Yahoo Finance](https://finance.yahoo.com/)의 코스피, 코스닥 자료를 이용하여 한국 주식 자료를 수집하였습니다. 수집한 데이터들은 Korea_Stock_since_2019, Korea_Stock_Full 두 폴더에서 관리하는데 휴일을 제외하고 매일 갱신됩니다.

## 주식 자료에 대한 간단한 소개

본 자료는 Yahoo Finance에서 한국 주식 데이터를 파이썬(Python)으로 크롤링하여 직접 수집한 것입니다. 크롤링에 이용하는 파일들은 CodeAndTool 폴더에 있습니다. 파이썬 코드 파일을 터미널로 실행하면 자동으로 자료를 크롤링하고 전처리하여 저장합니다.

일단 temp 폴더에 크롤링 된 주식 데이터가 저장됩니다. Korea_Stock_since_2019 폴더에는 2019년 이후 주식 파일들이 저장됩니다. Korea_Stock_Full 폴더에는 이전의 데이터와 지금까지의 데이터를 병합한 파일들이 저장됩니다.

## 다운 받은 주식 자료에 대한 참고

주식들은 거래정지와 상장 폐지되는 경우가 있습니다. 거래정지는 주식 거래가 금지된 경우를 말합니다. 거래정지가 된 주식은 일정 기간 거래가 없기에 데이터 또한 변화가 없습니다. 상장폐지의 경우 주식 거래가 종결되기 때문에 일반적으로 상장폐지가 결정된 날 이후로 데이터가 사라집니다. 이런 상황을 매일 점검하기 위해 현재[KRX 홈페이지](http://www.krx.co.kr/main/main.jsp)에서 [거래정지](http://marketdata.krx.co.kr/contents/MKD/04/0403/04030300/MKD04030300.jsp)와 [상장폐지](http://marketdata.krx.co.kr/contents/MKD/04/0406/04060600/MKD04060600.jsp) 목록을 확인하고 있습니다. 이렇게 확인된 목록을 total_stocklist.csv 파일에 당일의 상태열(col)로 만들고 있습니다. 이것은 해당 날짜에 크롤링할 주식 코드와 아닌 것을 구분하는 역할을 합니다.

크롤링을 하는 동안 야후와 서버 연결에 실패하는 경우가 있습니다. 그래서 코드 내에서 서버 에러가 난 주소들로 다시 한번 크롤링을 실행하지만, 그럼에도 불구하고 서버 연결에 실패하는 경우는 그 목록들을 모아 로그 파일(error_list.csv)에 저장합니다. 이 파일들을 가지고 해당 주식의 데이터를 수동으로 수집하거나 코드를 다시 한번 실행하여 문제를 해결할 수 있습니다.

제가 자료를 갱신할 때 [github 이슈](https://github.com/choosunsick/Korea_Stocks/issues)를 통해 당일에 크롤링 되는 주식과 크롤링이 되지 않은 주식(거래정지와 상장 폐지된 것을 포함한 야후의 서버 에러로 크롤링에 실패한 목록)을 올릴 예정입니다.

추가로 이 깃허브의 자료 중 코스닥에 상장된 일부 주식들은 현재 야후에서 과거 데이터가 보이지 않아서 불완전한 경우가 있습니다. Korea_Stock_since_2018 파일에 있는 주식 데이터 중 코스닥에 상장된 주식들의 경우 2018-3-7일의 데이터가 유실되어 없습니다. 그 외에 일부 주식들의 경우는 야후 파이낸스에 데이터가 나오지 않는 관계로 크롤링 되지 않습니다. 예를 들어 주식 한국ANKOR유전(152550), 하나니켈1호(099340), 하나니켈2호(099350), 베트남개발1(096300), 한국패러랠(168490) 등이 있습니다. 효성중공업(298040)은 야후 파이낸스에서 데이터가 보이지 않았지만, 현재(2018-08-20) 버그가 고쳐져 데이터가 나와 크롤링이 가능합니다. Korea_Stock_Full 파일에서 주식 파일들의 2018년 이전 데이터는 인터넷을 통해 구한 것으로 [gomjellie의 깃허브](https://github.com/gomjellie/kospi-kosdaq-csv) 사이트를 참고했습니다.

## 직접 주식 데이터를 받는 방법  

현 상태에서 직접 주식 데이터를 다운 받고 싶은 경우 다음과 같은 과정을 통해 자료를 크롤링할 수 있습니다. 기본적으로 파이썬이 3.5 이상의 버전이라면 코드를 사용할 수 있습니다. 그러나 만약 파이썬 버전이 3.5보다 낮다면 파이썬의 버전을 3.5이상으로 업데이트 해주셔야합니다. 파이썬 3.5이상 버전이 준비되면, 제 깃허브의 자료를 복제(cloan)하거나 다운받습니다. 다운이 완료됐을 경우 현재까지 주식 데이터 파일과 코드를 실행시키는데 필요한 자료들이 들어옵니다. 추가로 주식 데이터들은 한번 받으면 추가로 다운 받을 필요는 없습니다만 갱신을 하기 위해서는 매일매일 total_stocklist.csv 파일을 다운받아 갱신해야 합니다.

당일의 주식시장이 마감된 시각인 4시 이후에 터미널을 작동하여 파이썬 스크립트 파일을 실행시키면 됩니다. 시간에 따라서 html이 들어오지 않는 경우가 있으니 반드시 장 마감 시각 이후에 크롤링을 해야합니다.

## 다운 받은 주식 자료를 활용하는 방법

위와 같이 다운받은 주식 자료를 R 코드를 통해 5개 주식의 포트폴리오 최적화와 단순 포트폴리오를 비교해 보겠습니다. 참고로 아래의 코드들은 sample.R 파일을 중심으로 만든 것입니다. 본격적으로 들어가기에 앞서 포트폴리오와 그것의 최적화는 무엇을 의미하는지 설명하겠습니다.

포트폴리오란 일반적으로 투자하는 대상들의 집합을 의미합니다. 예를 들면 어떤 사람이 주식과 부동산, 금이나 은 같은 현물 자산 등에 나누어 투자한다고 할 때 이 사람은 포트폴리오를 가지고 있는 것이라 말할 수 있습니다. 물론 주식에만 투자한다고 할 경우에도 포트폴리오를 가질 수 있는데, 이 경우에는 다양한 종목에 나누어 투자하는 경우를 의미합니다. 이런 포트폴리오 정의에 따를 때 포트폴리오 최적화란 포트폴리오가 가능한 기대수익률과 위험 수준에 대한 가장 적절한 투자 비율을 구하는 것을 의미합니다.

예를 들면 5개 주식에 총 1000만원을 투자한다고 할 경우 금액을 나누는 비중은 다양한 경우가 나올 수 있습니다. 일반적으로 5개 주식에 모두 공평하게 투자 비율을 둔다고 하면 1000만원에 20%씩 각 주식에 대한 투자금액은 200만원이 됩니다. 이와 같이 각 주식에 대해 투자 비율을 무작위로 정하는 것을 단순 포트폴리오라 합니다. 그렇다면 과연 스스로 투자 비율을 정할 때 얻을 수 있는 포트폴리오의 기대수익률과 위험 수준이 최고로 좋은 것일까요? 아니면 최적의 투자 비율을 정한다면 더 높은 기대수익률과 더 낮은 위험 수준을 얻을 수 있지 않을까요?

### 주식 자료 읽어와서 수익률 구하기

먼저 5개 주식 데이터를 읽어옵니다. 저는 포스코, LG전자, SK하이닉스, 네이버, 현대건설을 선택했습니다. 포트폴리오를 구성하는 주식 데이터는 같은 기간을 뽑아 왔어도 거래 정지등의 이유로 자료의 숫자가 서로 다를 수 있습니다. 참고로 밑의 코드에서는 약 5년간의 일간 자료를 읽어옵니다. 데이터들의 숫자가 서로 다르기 때문에 월간형식으로 바꾸어줍니다. 그 외에 부족한 데이터가 있는 부분에 해당 자료의 평균값을 넣거나 결측치를 처리하는 다양한 방법으로 데이터의 수를 맞추어 줄 수 있습니다. 단 이런 방법들을 적용했음에도 데이터의 수가 서로 차이가 난다면 포트폴리오를 구성하는 종목을 바꿔야 합니다.  

```
install.packages("xts")
library(xts)
install.packages("quantmod")
library(quantmod)

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

```

자료를 단순히 `read.csv()`함수로 읽어도 되지만, 디렉토리 문제를 피해가기 위해 새롭게 함수를 만들었습니다. 이 함수에서는 단순히 자료를 읽어오는 것과 함께 자료의 월율화가 이루어집니다. 월율화란 일간 자료를 월간 형식의 자료로 바꿔주는 것을 말합니다. 위 코드에서는 일간 수정 종가자료를 월간 수익률의 형식으로 바꿉니다. 이제 함수에 필요한 주식 코드만 입력하면 자료를 바로 읽어올 수 있게 됩니다.

```
stock_list <- c("005490","066570","000660","035420","000720")
stock_data <- do.call(cbind,lapply(stock_list,FUN = function(i){read.file(i)}))
colnames(stock_data)<- stock_list

```

앞서 만든 `read.file()` 함수를 필요한 주식 코드별로 적용해 하나의 데이터로 만들어 줍니다. 데이터가 준비되었으니 투자 비율을 랜덤하게 적용해 단순 포트폴리오를 그려볼 수 있습니다.

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

random_p<-ggplot(data = p_random,aes(x = pvol,y = pret))+geom_point(color="red")+
  labs(x = "expected_volatility",y="expected_return")+theme(legend.position = "none")
random_p

```

위 코드에서 포트폴리오의 평균 수익률과 공분산을 구해줍니다. 이것을 토대로 포트폴리오의 기대수익률과 분산의 계산을 반복해줍니다. 반복하는 이유는 가중치에 따라서 가능한 포트폴리오들이 다양하기 때문입니다. 가중치는 0~1 사이의 임의의 소수점으로 정해집니다. 여기서 가중치는 각 주식에 대한 투자 비율입니다. 이렇게 반복된 계산으로 구해진 기대 수익률(y)과 분산(x)의 집합들을 그리면 아래와 같이 나옵니다. 이 그래프를 무작위 포트폴리오가 그려진 것으로 단순 투자기회 집합이라 합니다. 참고로 아래의 그래프는 가중치가 무작위하게 정해지기 때문에 그릴 때 마다 점들의 위치가 달라질 수 있습니다.

![단순 투자기회 집합](https://user-images.githubusercontent.com/19144813/44709797-73b0cf00-aae5-11e8-80d6-0d4be166dc2d.jpeg)

이제 최적의 투자기회 집합 즉 효율적 투자선(efficient frontier)을 그려보겠습니다. 효율적 투자선은 같은 위험 수준 대비 최대 기대수익률 또는 같은 수익률 대비 최소 위험 수준을 가지는 투자 집합들을 말합니다. 아래 코드에서 가중치 계산과 관련된 부분은 [ggwlsrb블로그](http://blog.naver.com/PostView.nhn?blogId=ggwlsrb&logNo=220940357589&parentCategoryNo=&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView)를 참조 했습니다.

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
p<-ggplot(data = ptemp,aes(x = pvols,y = prets))+geom_point(color="blue")+
  labs(x = "expected_volatility",y="expected_return")+theme(legend.position = "none")

p+annotate("text",x = c(ptemp$pvols[which.min(ptemp$pvols)],ptemp$pvols[which.max(ptemp$shape.ratio)]), y = c(ptemp$prets[which.min(ptemp$pvols)],ptemp$prets[which.max(ptemp$shape.ratio)]), label=c("MVP","MSP"), col=c("black","red"))

```

![최적 투자기회 집합](https://user-images.githubusercontent.com/19144813/44709792-701d4800-aae5-11e8-9d09-4ae602abff21.jpeg)

이 그래프는 앞서 본 단순 투자기회 집합 그래프와 달리 특정한 형태를 보이는데, 곡선처럼 보이지만 실제로는 일정하게 배치된 점들이 연결된 것입니다. 위의 두 그래프에서 하나의 점은 하나의 포트폴리오를 의미하는데, 점의 x, y 좌표는 그 포트폴리오의 위험 수준과 기대수익률을 의미합니다.

이제 위의 두 그래프를 비교해봅시다. 첫 그래프는 단순 투자기회 집합을 그린 것으로 위험 수준은 최대 30%(0.3)까지 될 수 있습니다. 반면 두 번째 최적의 투자기회 집합 그래프는 위험 수준이 최대 28%(0.28) 정도까지 밖에 나오지 않습니다. 위험 수준의 차이가 별로 없어 보이지만 해당 위험 수준 대비 기대 수익률에서 큰 차이를 찾아볼 수 있습니다.

예를 들면 위험 수준이 20%(0.2)일 때 단순 투자기회 집합에서는 최대 기대수익률이 약 18%(0.18)밖에 안 되지만 최적의 투자기회 집합에서는 최대 22%(0.22)로 4%(0.04)나 차이가 납니다. 이러한 차이를 통해 보았을 때 개별 주식에 대한 투자 비율을 어떻게 정하는가가 기대수익률과 위험 수준에 영향을 준다는 것을 알 수 있습니다.

최적의 투자기회 집합 그래프에서 주목할 것은 MVP(Minimum Variance Portfolio)점과 MSP(Maximum Sharpe ratio Portfolio)점입니다. MVP는 최저 위험 수준일 때의 최대 기대수익률을 보여주는 점입니다. 이 점 위의 점들은 모두 특정한 위험 수준에 대한 최대 기대수익률을 나타내는 점입니다. 그중에서도 MSP는 최대 샤프지수일 때의 점을 의미합니다. [샤프지수(sharp.ratio)](https://ko.wikipedia.org/wiki/%EC%83%A4%ED%94%84_%EB%B9%84%EC%9C%A8)가 무엇인지 알고 싶으시면 링크를 참조하시면 됩니다. 물론 위 코드에서 샤프지수를 계산할 때 편의상 무위험 수익률을 0으로 설정하여 계산했습니다.

이제 최적의 투자 비율일 때가 무작위로 투자 비율을 정했을 때보다 나은지 비교해보겠습니다.
단순하게 투자 비율을 모두 같게 했을 때와 최대 샤프 비율일 때의 투자 비율과 기대수익률, 위험 수준 값을 비교하겠습니다. 아래의 코드는 투자 비율이 모두 20%일 때의 기대수익률과 위험 수준을 구하는 코드입니다.

```
t(matrix(0.2,ncol = 1,nrow = 5))%*%mu
sqrt(t(matrix(0.2,ncol = 1,nrow = 5))%*%sigma%*%matrix(0.2,ncol = 1,nrow = 5))

```

위 코드의 결과를 보면 기대수익률은 약 13%와 위험 수준은 16%가 나옵니다. 반면에 최대 샤프 비율 일때의 기대수익률과 위험 수준은 다음과 같습니다.

```
weight_data[which.max(ptemp$shape.ratio),]
ptemp[which.max(ptemp$shape.ratio),]

```

위 코드에서 투자 비율은 약 15%, -2%, 55%, 26%, 5%로 나옵니다. 참고로 이때 투자 비율이 음수인 것은 공매도를 의미합니다. 이 투자 비율을 지닌 포트폴리오의 기대수익률은 약 20%이고 위험 수준은 약 17%입니다. 각각의 결과를 비교해보면, 기대수익률은 대략 7%가 올라갔지만, 위험 수준은 1%밖에 차이가 나지 않아 서로 비슷한 수준에서 머물고 있음을 확인할 수 있습니다.

맨위의 예시를 적용해보면 각 주식에 200만원씩 투자하는 것보다 150만원, 0원, 550만원, 250만원, 50만원으로 투자를 하는게 비슷한 위험 수준을 가지면서 7% 더 높은 기대수익률을 얻을 수 있다는 것입니다. 이 비교에 따라 투자 비율을 최적화 하는 것이 임의로 투자 비율을 결정하는 것보다 더 좋은 선택인 것을 알 수 있습니다. 즉 포트폴리오의 최적화를 통해 같은 기대수익률 대비 최저 위험 수준 혹은 같은 위험 수준 대비 최대 기대수익률을 가진 포트폴리오들을 찾아볼 수 있습니다.
