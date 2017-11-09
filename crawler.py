import requests
import json
from bs4 import BeautifulSoup as bs

url_base = "https://www.dhgate.com/wholesale/cell-phones-smartphones/c105008"


def getImageURL(item):
    imageTag = item.select("img")

    # if imageTag is not empty
    if imageTag:
        imageTag[0] = imageTag[0]['src']
    else:
        imageTag.append(item.select(".photo")[0].find('a')['lazyload-src'])
    
    return imageTag[0]


def getProductInfo(url):

    res = requests.get(url)
    soup = bs(res.text,"html.parser")

    wprice = soup.select(".wprice-line")[0].select(".js-wholesale-list")[0].find_all('li')

    # product amount and the price
    for w in wprice:
        print (w['nums'])
        print (w['price'])



for i in range(0,5):

    if i!=0:
        url = url_base + "-" + '{}'.format(i)
    else:
        url = url_base

    url = url + ".html"

    res = requests.get(url);


    soup = bs(res.text,"html.parser")
    listitem = soup.find_all("div",class_="listitem")
    for idx, item in enumerate(listitem):
        
        # the rest of items are advertisements
        if idx == 24:
            break
        
        # product name
        print (item.select(".pro-title")[0].text)
        
        # product image url
        imageURL = "http:" + getImageURL(item)
        print (imageURL)
        
        # request to product info
        productURL = "http:" + item.select(".pro-title")[0].find('a').get('href')
        getProductInfo(productURL)

