#!/usr/local/opt/python/bin/python3.7

import asyncio
import aiohttp
from aiohttp import ClientSession
import json
import pandas as pd
import os
from datetime import datetime

total_code = pd.read_csv("total_stocklist.csv")

today = datetime.today().strftime("%Y %m %d")
today_normal_list = total_code[total_code[str.replace(today," ","_")]=="normal"]

normal_list_fullcode =[]

normal_list_fullcode =[]
for i in today_normal_list.code:
    normal_list_fullcode.append(str(i).zfill(6))

pd.options.mode.chained_assignment = None

today_normal_list.code = normal_list_fullcode

kospi_normal_list=today_normal_list[today_normal_list.구분=="Kospi"]
kosdaq_normal_list=today_normal_list[today_normal_list.구분=="Kosdaq"]

ks_urls = []
for x in kospi_normal_list.code:
    url = 'https://finance.yahoo.com/quote/'+str(x)+'.KS/history?p='+ str(x) + '.KS'
    ks_urls.append(url)

kq_urls = []
for x in kosdaq_normal_list.code:
    url = 'https://finance.yahoo.com/quote/'+str(x)+'.KQ/history?p='+ str(x) + '.KQ'
    kq_urls.append(url)

full_urls = ks_urls+kq_urls

urls_25 = []
for i in range(0,int(len(full_urls)/25)):
    x=list(range(0,len(full_urls)+1,25))
    urls_25.append(full_urls[x[i]:x[i+1]])

urls_25.append(full_urls[-(len(full_urls)-(int(len(full_urls)/25)*25)):])    
    
html_dict = {}
not_error_urls = []
error_urls = []
new_yahoo_error=[]

async def fetch(session,url):
    bounde_sempahore = asyncio.BoundedSemaphore(200)
    async with bounde_sempahore:
        async with await session.get(url,timeout=30,allow_redirects=True) as response:
            print(response.status)
            if response.status == 404:
                await asyncio.sleep(60)
            return await response.text()

new_yahoo_error=[]
def html_clean(html_dict):
    for i in range(0,len(html_dict)):
        print(list(html_dict.keys())[i])
        html = list(html_dict.values())[i]
        temp1 = html.split('\"HistoricalPriceStore\":')[1] 
        temp2 = temp1.split('],"isPending":false,"')[0]
        temp3 = json.dumps(temp2)
        temp4 = temp3.replace('\\','')[11:]
        yahoo_json = json.loads((temp4[:len(temp4)-1]+']'))
        test = json.dumps(yahoo_json)
        test = pd.read_json(test, orient='records')
        if len(test)==0:
            print("nodata on yahoo")
            new_yahoo_error.append(list(html_dict.keys())[i])
            pass
        else:
            test2 = pd.concat([test['open'][:30], test['high'][:30],test['low'][:30],test['close'][:30],test['volume'][:30],test['adjclose'][:30]], axis=1).fillna(0).astype(int)
            test2 = test2.set_index(test['date'][:30])
            test2.index = test2.index[:].strftime("%Y-%m-%d")
            test2.columns = ['Open','High','Low','Close','Volume','Adj_Close']
            savename = "../temp/"+list(html_dict.keys())[i]+".csv"
            test2.to_csv(savename,index_label='Date')

async def get_site_content(url):
    conn = aiohttp.TCPConnector(limit=None)
    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            text = await fetch(session, url)
        except:    
            print("connection_fail")
        else:
            if len(text.split('\"HistoricalPriceStore\":'))==2:
                not_error_urls.append(url)
                #print(url)
                return html_dict.update({url[-9:-3]:text})
            else:
                error_urls.append(url) 
    
async def task(urls):
    return await asyncio.wait([get_site_content(i) for i in urls])

def cover(urls):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task(urls))
    loop.close()

[cover(url) for url in urls_25]

html_clean(html_dict)


html_dict = {}

server_error_urls = [x for x in full_urls if x not in not_error_urls]
        

if len(server_error_urls)!=0:
    cover(server_error_urls)
    html_clean(html_dict)

final_error_urls = []
if len(not_error_urls)!=len(full_urls):
    for x in full_urls:
        if x not in not_error_urls:
            final_error_urls.append(x)
else:
    final_error_urls = []
    print("no remain urls")


date = datetime.today().strftime("%m %d")
date = str.replace(date," ","_")

error_list = pd.DataFrame({"urls":final_error_urls})
error_list.to_csv("./"+"error_list_" + date + ".csv",index=False)

crawling_list = pd.DataFrame({"urls":not_error_urls})
crawling_list.to_csv("./"+"crawling_list_"+  date + ".csv",index=True)

if len(new_yahoo_error)==0:
    print("no new error")
else:
    temp_yahoo_error_list =  pd.DataFrame({"urls":new_yahoo_error})
    temp_yahoo_error_list.to_csv("./"+"new_yahoo_error_list"+  date + ".csv",index=True)


def mergeStock(stockNumber):
    """
    기존에 파일이 없는 신규 상장의 경우를 고려해서 try와 except를 사용 
    """
    try:
        tempPath ="../Korea_Stocks_since_2019/"  + stockNumber
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
        savename = "../Korea_Stocks_since_2019/"+stockNumber
        stockData.to_csv(savename,index_label='Date')
    except:
        tempPath = "../temp/" + stockNumber 
        stockData_new = pd.read_csv(tempPath, index_col=0, parse_dates=True, dayfirst=True)
        stockData_new = stockData_new.sort_index()
        stockData_new = stockData_new.fillna(0.0).astype(int)
        stockData_new.columns = ['Open','High','Low','Close','Volume','Adj Close']
        stockData_new = stockData_new[['Open','High','Low','Close','Volume','Adj_Close']]
        savename = "../Korea_Stocks_since_2019/"+stockNumber
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


list1=os.listdir("../temp/")
list1=[s for s in list1 if "csv" in s]
for i in list1:
    mergeStock(i)
    merge_about_2000(i)
