import asyncio 
import pandas as pd
import aiohttp
import json
import os
from datetime import datetime

total_temp = pd.read_csv("total_stocklist.csv")

today_date = str.replace(datetime.today().strftime("%Y %m %d")," ","_")
normal_list_fullcode =[]
for i in total_temp['code']:
    normal_list_fullcode.append(str(i).zfill(6))

test_json={}
for i in range(0,len(total_temp)):
    if total_temp['구분'][i]=='Kospi':
        KS_KQ="KS"
    else:
        KS_KQ="KQ"
    test_json.update({normal_list_fullcode[i]:{'name':total_temp.name[i],'is_KS':KS_KQ,'Date':{today_date:total_temp[today_date][i]}}})

test12 = [{'code':i,'KS&KQ':j['is_KS']} for i,j in test_json.items() if j['Date'][today_date] == 'normal']

temp_15 = []

for i in range(0,int(len(test12)/15)):
    x=list(range(0,len(test12)+1,15))
    temp_15.append(test12[x[i]:x[i+1]])    

temp_15.append(test12[-(len(test12)-(int(len(test12)/15)*15)):])  

def parse_html(text):
    try:
        stock_number = text.split("symbol")[0].split("title")[1].split(" (")[1].split(") ")[0].split(".")[0]
    except:
        stock_number = text.split("url")[1].split("/")[3].split(".")[0]
    finally:
        stock_number_str = f'{stock_number}.csv'
        temp1 = text.split('\"HistoricalPriceStore\":')[1].split('],"isPending":false,"')[0] 
        temp1 = json.dumps(temp1)
        temp1 = temp1.replace('\\','')[11:]
        yahoo_json = json.loads((temp1[:len(temp1)-1]+']'))
        return{"json":yahoo_json,"stock_number":stock_number_str}

def write_csv(yahoo_json):
    test = json.dumps(yahoo_json['json'])
    test = pd.read_json(test, orient='records')
    test2 = pd.concat([test['open'][:30], test['high'][:30],test['low'][:30],test['close'][:30],test['volume'][:30],test['adjclose'][:30]], axis=1).fillna(0).astype(int)
    test2 = test2.set_index(test['date'][:30])
    test2.index = test2.index[:].strftime("%Y-%m-%d")
    test2 = test2[['open','high','low','close','volume','adjclose']]
    test2.columns = ['Open','High','Low','Close','Volume','Adj_Close']
    test2 = test2[(test2.T != 0).any()]
    savename = f"../temp/{yahoo_json['stock_number']}"
    test2.to_csv(savename,index_label='Date')

error_list_404 = []

def stock_download(code_list):

    results = []

    async def download(code: str, KSorKQ:str):
        bounde_sempahore = asyncio.BoundedSemaphore(100)
        conn = aiohttp.TCPConnector(limit=None)
        async with aiohttp.ClientSession(connector=conn) as session:
            async with bounde_sempahore:
                async with session.get(f'https://finance.yahoo.com/quote/{code}.{KSorKQ}/history?p={code}.{KSorKQ}',allow_redirects=True,timeout=100) as resp:
                    print(resp.status)
                    try:
                        results.append({'code': code, 'text': await resp.text(), "KS&KQ":KSorKQ})
                    except:
                        error_list_404.append({'code':code,"KS&KQ":KSorKQ})

    tasks = [download(item['code'], item['KS&KQ']) for item in code_list]

    asyncio.run(asyncio.wait(tasks))
    return{'result':results,'error_list':error_list_404}

error_list = []

def full_stack(code_list):
    temp = stock_download(code_list)
    for item in temp['result']:
        try:
            write_csv(parse_html(item['text']))
        except:
            error_list.append({'code':item['code'],"KS&KQ":item['KS&KQ']})
        
    return error_list

new_error_list = []
def retry_error_list(error_list):
    if len(error_list)!=0:
        temp = stock_download(error_list)
        for item in temp['result']:
            try:
                write_csv(parse_html(item['text']))
            except:
                new_error_list.append(error_list)
    
    return new_error_list
    


def mergeStock(stockNumber):
    """
    기존에 파일이 없는 신규 상장의 경우를 고려해서 try와 except를 사용 
    """
    try:
        tempPath ="../Korea_Stocks_since_2020/"  + stockNumber
        stockData = pd.read_csv(tempPath, index_col=0, parse_dates=True, dayfirst=True)
        tempPath = "../temp/" + stockNumber 
        stockData_new = pd.read_csv(tempPath, index_col=0, parse_dates=True, dayfirst=True)
        stockData_new = stockData_new.sort_index()
        stockData_new.columns = ['Open','High','Low','Close','Volume','Adj_Close']
        stockData_new = stockData_new[['Open','High','Low','Close','Volume','Adj_Close']]
        stockData = stockData.append(stockData_new,sort=True)
        stockData = stockData[~stockData.index.duplicated(keep='last')]
        stockData = stockData.sort_index()
        stockData = stockData.fillna(0.0).astype(int)
        stockData = stockData[['Open','High','Low','Close','Volume','Adj_Close']]
        savename = "../Korea_Stocks_since_2020/"+stockNumber
        stockData.to_csv(savename,index_label='Date')
    except:
        tempPath = "../temp/" + stockNumber 
        stockData_new = pd.read_csv(tempPath, index_col=0, parse_dates=True, dayfirst=True)
        stockData_new = stockData_new.sort_index()
        stockData_new = stockData_new.fillna(0.0).astype(int)
        stockData_new.columns = ['Open','High','Low','Close','Volume','Adj_Close']
        stockData_new = stockData_new[['Open','High','Low','Close','Volume','Adj_Close']]
        savename = "../Korea_Stocks_since_2020/"+stockNumber
        stockData_new.to_csv(savename,index_label='Date')

def merge_about_2000(stockNumber):
    try:
        tempPath ="../Korea_Stocks_Full/" + stockNumber
        stockData = pd.read_csv(tempPath, index_col=0, parse_dates=True, dayfirst=True)
        stockData = stockData[['Open','High','Low','Close','Volume','Adj_Close']]
        stockData = stockData.sort_index()
        tempPath = "../temp/" + stockNumber 
        stockData_new = pd.read_csv(tempPath, index_col=0, parse_dates=True, dayfirst=True)
        stockData_new = stockData_new.sort_index()
        stockData_new.columns = ['Open','High','Low','Close','Volume','Adj_Close']
        stockData_new = stockData_new[['Open','High','Low','Close','Volume','Adj_Close']]
        stockData = stockData.append(stockData_new,sort=True)
        stockData = stockData[~stockData.index.duplicated(keep='last')]
        stockData = stockData.fillna(0.0).astype(int)
        stockData = stockData.sort_index()
        stockData = stockData[['Open','High','Low','Close','Volume','Adj_Close']]
        savename = "../Korea_Stocks_Full/"+stockNumber
        stockData.to_csv(savename,index_label='Date')
    except:
        tempPath ="../temp/"  + stockNumber
        stockData = pd.read_csv(tempPath, index_col=0, parse_dates=True, dayfirst=True)
        stockData = stockData.sort_index()
        stockData = stockData.fillna(0.0).astype(int)
        stockData.columns = ['Open','High','Low','Close','Volume','Adj_Close']
        stockData = stockData[['Open','High','Low','Close','Volume','Adj_Close']]
        savename="../Korea_Stocks_Full/"+stockNumber
        stockData.to_csv(savename,index_label='Date')

for i in temp_15:
    full_stack(i)

print(len(error_list))
print(len(error_list_404))

retry_error_list(error_list)
final_error_list = retry_error_list(error_list_404)

date = str.replace(today_date,"_","-")

list1=os.listdir("../temp/")
list1=[s for s in list1 if "csv" in s]
re_list = []
for i in list1:
    temp = pd.read_csv(f"../temp/{i}",index_col=0, parse_dates=True, dayfirst=True)
    if date not in temp.index:
        re_list.append(i)

    mergeStock(i)
    merge_about_2000(i)

date_false = pd.DataFrame({"code":re_list})
date_false.to_csv("./"+"date_error_" + date + ".csv",index=False)