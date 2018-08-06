import asyncio
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import json
import pandas as pd

kospi_list=pd.read_csv("kospiList_180801.csv")
now_kospi_able=kospi_list[kospi_list.ingornot=="ing"]
KS_full_code = []

for x in now_kospi_able.code:
    if len(str(x))==2:
        KS_full_code.append("0000"+str(x))
    elif len(str(x))==3:
        KS_full_code.append("000"+str(x))
    elif len(str(x))==4:
        KS_full_code.append("00"+str(x))
    elif len(str(x))==5:
        KS_full_code.append("0"+str(x))
    else:
        KS_full_code.append(str(x))

urls = []
for x in KS_full_code:
    url = 'https://finance.yahoo.com/quote/'+str(x)+'.KS/history?p='+ str(x) + '.KS'
    urls.append(url)

urls_25 = []
for i in range(0,31):
    x=list(range(0,len(urls)+1,25))
    urls_25.append(urls[x[i]:x[i+1]])


html_dict ={}

def cover(urls):
    async def get_site_content(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.read()
                print(url[-9:-3])
                soup4 = BeautifulSoup(text, "html.parser")
                temp = soup4.text.strip()
        return html_dict.update({url[-9:-3]:temp})
    contents = [get_site_content(url) for url in urls]
    loop = asyncio.get_event_loop()
    task = asyncio.wait(contents)
    loop.run_until_complete(task)
    def html_clean(html_dict):
        for i in range(0,len(html_dict)):
            html = list(html_dict.values())[i]
            temp1 = html.split('\"HistoricalPriceStore\":')[1] 
            temp2 = temp1.split('],"isPending":false,"')[0]
            temp3 = json.dumps(temp2)
            temp4 = temp3.replace('\\','')[11:]
            yahoo_json = json.loads((temp4[:len(temp4)-1]+']'))
            test = json.dumps(yahoo_json)
            test = pd.read_json(test, orient='records')
            test2 = pd.concat([test['open'][:30], test['high'][:30],test['low'][:30],test['close'][:30],test['volume'][:30],test['adjclose'][:30]], axis=1).fillna(0.0).astype(int)
            test2 = test2.set_index(test['date'][:30])
            test2.index = test2.index[:].strftime("%Y-%m-%d")
            savename = "/Users/choosunsick/Desktop/Korea_Stocks/Code&Download_file/download/"+list(html_dict.keys())[i]+".csv"
            test2.to_csv(savename,index_label='Date')
    return html_clean(html_dict)

#[cover(url) for url in urls_25]
for url in urls_25:
    print(url)
    cover(url)
