import requests
import json
from bs4 import BeautifulSoup as bs

url_base = "https://www.dhgate.com/wholesale/cell-phones-smartphones/c105008"


for i in range(0,1):

    if i!=0:
        url = url_base + "-" + '{}'.format(i)
    else:
        url = url_base

    url = url + ".html"

    res = requests.get(url);


    soup = bs(res.text,"html.parser")
    for idx, item in enumerate(soup.find_all("div",class_="listitem")):
        
        if idx == 24:
            break
        
        print (item.select(".pro-title")[0].text)
        
        res2 = requests.get("http:"+ item.select(".pro-title")[0].find('a').get('href'))
        soup2 = bs(res2.text,"html.parser")
        wprice = soup2.select(".wprice-line")[0].select(".js-wholesale-list")[0].find_all('li')
#         print (wprice)
        
        for w in wprice:
#             print (w)
            print (w['nums'])
            print (w['price'])

