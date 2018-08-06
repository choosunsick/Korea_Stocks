import asyncio
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import json
import pandas as pd


kosdaq_list=pd.read_csv("kosdaqList_180801.csv")
now_kosdaq_able=kosdaq_list[kosdaq_list.ingornot=="ing"]

KQ_full_code = []

for x in now_kosdaq_able.code:
    if len(str(x))==2:
        KQ_full_code.append("0000"+str(x))
    elif len(str(x))==3:
        KQ_full_code.append("000"+str(x))
    elif len(str(x))==4:
        KQ_full_code.append("00"+str(x))
    elif len(str(x))==5:
        KQ_full_code.append("0"+str(x))
    else:
        KQ_full_code.append(str(x))



kq_urls = []
for x in KQ_full_code:
    url = 'https://finance.yahoo.com/quote/'+str(x)+'.KQ/history?p='+ str(x) + '.KQ'
    kq_urls .append(url)

urls_30 = []
for i in range(0,41):
    x=list(range(0,len(kq_urls)+1,30))
    urls_30.append(kq_urls[x[i]:x[i+1]])

urls_30.append(kq_urls[-(len(kq_urls)-(round(len(kq_urls)/30)*30)):])


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
            savename = "/Users/choosunsick/Desktop/Korea_Stocks/Code&Download/download/"+list(html_dict.keys())[i]+".csv"
            test2.to_csv(savename,index_label='Date')
    return html_clean(html_dict)

[cover(url) for url in urls_30]
