# 깃허브 설명

안녕하세요. 팀LOPES의 추선식입니다. 저희 팀에서 주식과 관련된 프로젝트를 하면서 차트 분석을 비롯한 여러가지 분석을 위한 데이터가 필요하게 되었습니다. 이와 더불어 시중에서는 주식의 수치들을 눈으로 확인할 수 있지만 직접적인 수치를 다루어 데이터를 만질 수 없기 때문에 주식 데이터를 직접 모으고 관리하려 합니다. [Yahoo Finance](https://finance.yahoo.com/)의 코스피, 코스닥 자료를 이용하여 한국 주식 데이터를 수집하였습니다. 수집한 데이터들은 Korea_Stock_since_2018, Korea_Stock_Full 두 폴더에서 관리하는데 휴일을 제외하고 매일 갱신됩니다.

## 간단한 자료 소개

본 자료는 Yahoo Finance에서 한국 주식 데이터를 파이썬(Python)으로 크롤링하여 직접 수집한 것입니다. 크롤링하는 파이썬 코드 파일과 그것을 사용하는 데 필요한 파일들은 CodeAndTool 폴더에 있습니다. 파이썬 코드 파일을 터미널로 실행하면 자동으로 자료를 크롤링하고 전처리하여 저장합니다.

크롤링 된 주식 데이터는 temp 폴더에 저장됩니다. 이 자료들을 2018년 주식 데이터와 결합하여 저장한 파일들이 Korea_Stock_since_2018 폴더에 저장됩니다. Korea_Stock_Full 폴더에는 2018년 이전의 데이터와 지금까지의 데이터를 병합한 파일들이 저장됩니다.

## 자료에 대한 참고
모든 코스피와 코스닥 주식이 크롤링되는 것이 아니기 때문에 거래정지와 상장폐지되는 주식들의 목록이 필요합니다. 거래정지는 주식의 거래가 금지된 경우를 말합니다. 거래정지가 된 주식은 일정기간 동안 거래가 없기에 데이터 또한 변화가 없습니다. 상장폐지의 경우 주식 거래가 종결되기 때문에 상장폐지가 결정된 날 이후로 해당 주식에 대한 데이터가 사라집니다. 이런 상황을 매일 체크해야 합니다. 따라서 현재 [KRX 홈페이지](http://www.krx.co.kr/main/main.jsp)에서 [거래정지](http://marketdata.krx.co.kr/contents/MKD/04/0403/04030300/MKD04030300.jsp)와 [상장폐지](http://marketdata.krx.co.kr/contents/MKD/04/0406/04060600/MKD04060600.jsp) 목록을 확인할 수 있습니다. 확인된 목록을 total_stocklist.csv 파일에 당일의 상태열(col)로 만들고 있습니다. 이것은 해당 날짜에 크롤링할 주식 코드와 아닌 것을 구분하는 역할을 합니다.

야후의 서버 연결 문제는 코드가 실행되는 중에 가끔 야후와 서버 연결에 실패하여 주식 데이터가 크롤링 되지 않은 경우를 말합니다. 크롤링하는 과정에서 네트워크와 관련되어 있어 서버 연결에 실패하기 때문입니다. 물론 코드 내에서 서버 에러가 난 주소들을 모아서 다시 한번 크롤링을 실행합니다.

그럼에도 불구하고 서버 에러가 나는 경우는 로그 파일(error_list.csv)로 저장됩니다. 이 파일을 가지고 해당 주식의 데이터를 수동으로 수집하거나 코드를 다시 한번 실행시키는 것으로 문제를 해결할 수 있습니다. 이와 함께 [github 이슈](https://github.com/choosunsick/Korea_Stocks/issues)를 통해 당일에 크롤링 되는 주식과 크롤링이 되지 않은 주식(거래정지와 상장 폐지된 것을 포함한 야후의 서버 에러로 크롤링에 실패한 목록)을 올릴 것입니다.

추가로 현재 자료 중 코스닥의 경우는 야후에서 과거 데이터를 저장하지 않기에 데이터가 없습니다. 따라서 일부 코스닥 데이터의 경우 불완전한 경우가 있습니다. Stock_since_2018 파일에 있는 주식 데이터 중 코스닥의 경우 3/7일의 데이터가 유실되어 없습니다. 그 외에 코스피의 주식 코드 298040, 152550, 099340, 099350, 096300, 168490 등의 경우 야후 파이낸스에 데이터가 나오지 않는 관계로 크롤링 되지 않습니다. Stock_about_2000 파일에서 주식 파일들의 2018년 이전 데이터는 인터넷을 통해 구한 것으로 [깃허브](https://github.com/gomjellie/kospi-kosdaq-csv)사이트를 참고했습니다.

## 스스로 코드를 돌리는 방법

먼저 전체 주식 목록 데이터(total_stocklist.csv)를 이용해서 크롤링 가능한 코스피와 코스닥 주식들의 야후 주소를 만들어줍니다. 만들어진 주소들은 25, 30개씩 묶여서 데이터를 크롤링하고 저장하는 메인 함수(cover)의 인자로 사용됩니다. 메인 함수는 비동기식으로 크롤링하는 함수와 크롤링한 자료를 정리해서 저장하는 함수 두 가지로 구성되어 있습니다. 크롤링하는 함수는 asyncio 패키지를 이용해 들어온 주소들의 자료를 비동기식으로 크롤링합니다. 자료를 정리하고 저장하는 함수는 크롤링 된 html 형태의 자료를 파싱하여 일차적으로 JSON 형식으로 저장하고, 그것을 다시 Dataframe 형식으로 읽어와 열과 인덱스를 정리해서 저장하는 역할을 합니다.

잠깐 비동기식과 동기식 크롤링의 차이를 설명해보겠습니다. 예를 들어 동기식으로 크롤링하는 경우 여러 주소가 있으면 들어온 순서대로 하나의 주소부터 시작하여 하나씩 주식 데이터를 크롤링하게 됩니다. 그러나 비동기식으로 크롤링하는 경우 하나의 주소가 크롤링 되는 걸 기다리는 대신에 들어온 여러 주소를 한 번에 크롤링합니다. 이렇게 들어온 모든 주소가 크롤링 되면 먼저 그 순서대로 파싱하고 전처리하여 데이터를 저장합니다.

크롤링하는 과정 중에 야후 서버 연결 에러가 발생할 경우 해당 주소를 함수의 밖으로 빼서 따로 저장합니다. 이 목록들을 가지고 다시 한번 크롤링 함수를 실행시켜 줍니다. 함수 실행 이후에도 에러로 인해 크롤링에 실패한 경우는 검사를 통해 그 목록만 따로 저장됩니다. 물론 최종적으로 크롤링 된 목록 역시 따로 저장됩니다. 크롤링해서 만든 자료와 에러목록, 크롤링 된 목록 등이 만들어지면 이제 기존의 자료와 병합하는 코드가 실행됩니다.

기존 자료와의 병합은 2가지가 이루어집니다. 2018년도 자료만 붙은 것과 2018년도 이전의 자료가 붙은 것 두 자료에 새로 만든 자료를 병합해 저장합니다. 병합(merge)함수는 기존에 합쳐지는 경우와 자료가 새로 만들어지는 경우(신규 상장의 경우)를 try와 except 구문으로 나누어 작동합니다. 이 함수는 각 디렉토리에서 해당 주식 코드의 파일을 열고 서로 병합한 다음 각 index(행)와 colname(열이름)등을 고려하여 중복을 제거하고 고유한 데이터만 남기고 저장합니다.     

## R을 활용한 간단한 주식데이터 분석

자료를 통해 5개 주식의 포트폴리오 최적화와 2개 주식의 포트폴리오 최적화를 비교하는 것을 R코드로 구현해보았습니다. 포트폴리오 최적화를 비교를 통해 알 수 있는 점은 분산투자의 효용성을 확인할 수 있습니다. 즉 어떤 주식들 간에 최적투자 기회 집합이 그려지는 모양에 따라 분산투자 효과가 있는지 혹은 없는지를 알 수 있습니다.  

### 자료 읽어와서 수익률 구하기

먼저 5개 주식을 읽어와 줍니다. 저는 삼성전자,LG전자,SK하이닉스,네이버,현대건설을 선택해 자료를 읽었습니다. 자료를 선택할 때 포트폴리오를 구성하는 주식들 데이터를 같은 기간을 뽑아 왔어도 거래 정지등의 이유로 자료의 숫자가 서로 다를 수 있습니다. 그럴 경우 대비해 일간자료를 월간형식으로 바꾸어줍니다. 단 이 경우에도 월 기간이 서로 차이가 난다면 포트폴리오를 구성하는 종목을 바꾸어주어야 합니다.  

```
install.packages("xts")
library(xts)

read.file<-function(x){#x=파일이름
  filename <- paste("/Users/choosunsick/Desktop/Korea_Stocks/Korea_Stocks_Full/",x,".csv",sep = "")
  stockdata<-read.csv(file = filename,header =T,stringsAsFactors = F)
  colnames(stockdata)[1] <-"Date"
  stockdata <- stockdata[which(stockdata$Date =="2013-07-01"):which(stockdata$Date =="2018-07-31"),]
  stockdata <- as.xts(stockdata$Adj.Close,order.by =as.Date(stockdata$Date))
  return(stockdata)
}

samsung<-read.file("005930")
LG<-read.file("066570")
sk.hinix<-read.file("000660")
naver<-read.file("035420")
hyundai<-read.file("000720")
```
자료는 단순하게 csv로 읽어도 되지만 여기서는 함수를 만들어서 사용했습니다. 함수를 만든 이유는 디렉토리 문제를 피해가기 위해서 입니다. filename 변수에 자료가 있는 폴더의 절대주소를 넣어줌으로서 필요한 주식 코드만 입력하면 자료를 바로 읽어올 수 있게 됩니다. 이것을 통해 R의 디렉토리에 상관 없이 바로 자료를 읽을 수 있습니다. 저희는 종가의 조정값과 시계열 자료만 필요합니다. 따라서 추가적으로 함수에서는 읽어온 자료를 필요한 부분만 추출하여 월별 xts형식으로 바꾸어 줍니다.

```
install.packages("quantmod")
library(quantmod)

five_stock<-data.frame(samsung=apply.monthly(samsung,sum),lg=apply.monthly(LG,sum),sk=apply.monthly(sk.hinix,sum),naver=apply.monthly(naver,sum),hyundai=apply.monthly(hyundai,sum))

five_stock$Samsung_log_return<-c(0,log(five_stock$samsung/Lag(five_stock$samsung))[2:61])
#같은 방식으로 나머지 주식들의 로그 수익률을 구합니다.

#두개 주식의 경우

two_stock<-data.frame(samsung=apply.monthly(samsung,sum),naver=apply.monthly(naver,sum))
two_stock$Samsung_log_return<-c(0,log(two_stock$samsung/Lag(two_stock$samsung))[2:61])
two_stock$Naver_log_return<-c(0,log(two_stock$naver/Lag(two_stock$naver))[2:61])
```

이제 불러온 파일을 하나로 묶어줍니다. 그리고 앞으로 계산하는데 필요한 로그 수익률을 구해줍니다. 이 로그 수익률은 이후 포트폴리오의 기대수익률과 공분산등을 계산하는데 사용됩니다. 5개 주식일 때와 더불어 2개 주식일때도 마찬가지로 진행됩니다.

```

mu <- matrix(colMeans(five_stock[,6:10])*12,ncol = 1)
sigma <- as.matrix(cov(five_stock[,6:10])*12)
inv_sigma <- as.matrix(solve(sigma))
ivec <- rep(1,ncol(five_stock[,6:10]))

Mu.p <- runif(n = 500,min = 0,max = max(mu))
A<-matrix(c(t(mu)%*%inv_sigma%*%mu,t(ivec)%*%inv_sigma%*%mu,t(mu)%*%inv_sigma%*%ivec,t(ivec)%*%inv_sigma%*%ivec),2,2)

pvols<-NULL
prets<-NULL

# 두개 주식일 때

mu<-matrix(colMeans(two_stock[,c(3,4)])*12,ncol = 1)
sigma<-as.matrix(cov(two_stock[,c(3,4)])*12)
inv_sigma<-as.matrix(solve(sigma))
ivec<-rep(1,ncol(two_stock[,c(3,4)]))

Mu.p <- runif(n = 500,min = 0,max = max(mu))
A<-matrix(c(t(mu)%*%inv_sigma%*%mu,t(ivec)%*%inv_sigma%*%mu,t(mu)%*%inv_sigma%*%ivec,t(ivec)%*%inv_sigma%*%ivec),2,2)

pvols<-NULL
prets<-NULL

```

연간 기대수익률과 공분산, 공분산의 역행렬 등을 만듭니다. 그리고 포트폴리오의 가능한 기대수익률 범위를 만듭니다. 투자비중인 가중치 값을 계산하기 위한 행렬(A)을 만듭니다. 이제 가중치 값에 따라 계산될 변동성과 기대수익률을 저장할 비어있는 벡터 두개를 만들면 준비가 끝납니다.


```
for(i in 1:500){
  b<-matrix(c(Mu.p[i],1),ncol = 1)
  lambda <- solve(A,b)
  weight <-as.matrix(inv_sigma%*%(lambda[1]*mu+lambda[2]*ivec),ncol=1)
  prets<-c(prets,as.numeric(t(weight)%*%mu))
  pvols<-c(pvols,sqrt(as.numeric(t(weight)%*%sigma%*%weight)))
  ptemp<-data.frame(cbind(pvols,prets))
  ptemp$shape.ratio <- ptemp$pret/ptemp$pvol
}
```

남은 것은 복잡한 행렬 계산뿐 입니다. 이 반복문은 가능한 500개의 기대수익률 값에 대해 자동으로 변동성과 기대수익률 값을 계산해줍니다.

```
install.packages("ggplot2")
library(ggplot2)

p<-ggplot(data = ptemp,aes(x = pvols,y = prets))+geom_point(color="blue")+labs(x = "expected_volatility",y="expected_return")+theme(legend.position = "none")
p+annotate("text",x = ptemp$pvols[which.min(ptemp$pvols)],y = ptemp$prets[which.min(ptemp$pvols)],label="MVP")
+annotate("text",x = ptemp$pvols[which.max(ptemp$shape.ratio)],y = ptemp$prets[which.max(ptemp$shape.ratio)],label="MSP")

```
같은 계산과 플롯팅을 두 가지 주식일 때도 반복해줍니다.

이렇게 그려진 그림은 5개 주식을 가지고 투자할 수 있는 최적의 투자선과 2개 주식을 가지고 투자할 수 있는 최적의 투자선 보여줍니다. 여기서 MVP 값은 가장 적은 변동성일 때의 기대수익률을 나타냅니다. 이점의 위쪽으로 그려진 점들은 모두 특정한 위험수준에서 가장 높은 기대수익률 값을 보여줍니다. 반면 MVP 값 밑의 점들은 더 높은 변동성과 더 낮은 기대수익률을 보여줍니다.
MSP 값은 최대 샤프지수 값일 때의 점을 말합니다. 여기서 샤프지수는 간단하게 기대수익률/변동성이라 말할 수 있습니다. 본래 무위험 수익률이 필요하지만 간단하게 하기위해 0으로 가정했습니다.
즉 MVP점 위의 영역이 그려진다면 분산투자가 잘되는 포트폴리오라고 말할 수 있습니다. 반면 MVP점 밑의 영역으로 그려진다면 분산투자를 하여도 효과가 미미하다는 것을 알 수 있습니다. 각각의 경우는 5가지 주식의 그림과 2개 주식일 때의 그림에서 잘 드러납니다.

![two_stock](https://user-images.githubusercontent.com/19144813/44260987-2a44c200-a251-11e8-8d2e-fb20f2d637a8.jpeg)

![five_stock](https://user-images.githubusercontent.com/19144813/44261008-3c266500-a251-11e8-9c8f-78d6aa096176.jpeg)
