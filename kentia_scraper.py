import requests
from bs4 import BeautifulSoup as BS
import os
import openpyxl as xl
from time import sleep, perf_counter
import pprint as pp




def getproductlink(url, productcode):
    print(f"Requesting link: {url}{productcode}")
    content = BS(requests.get(f"{url}{productcode}").text, 'html.parser')
    try:
        return content.select("div.image a")[0].get('href')
    except:
        pass


def getimagelinks(url):
    content = BS(requests.get(url).text, 'html.parser')
    result = list({*content.select("a.swiper-slide"), *content.select("div.image-gallery a")})
    return result

def getimagecontent(i, url, productcode):
    with open(os.getcwd() + "\\images\\" + str(productcode) + "_" + str(i) + ".jpg", 'wb') as f:
        f.write(requests.get(url).content)

wb = xl.load_workbook('kentia-2022-12-27-diff(2)-v2.xlsx')
sheet = wb['CMSInput']
url = 'https://www.kentia.gr/el/product-search?search='

length = 1
while sheet['b'+str(length+1)].value:
    length += 1

start = perf_counter()

f = open('log_failed.txt', 'w')
offset = 2
while sheet['b'+str(offset)].value:
    # sleep(2)
    offset += 1
    productcode = sheet['b'+str(offset)].value
    print(f'Downloading item {productcode}, {offset-2}/{length}')
    if not productcode:
        continue
    productlink = getproductlink(url, productcode)
    if not productlink:
        print(f'product link not found, logging {productcode=}')
        f.write(f"{productcode}'\n'")
        continue
    imagelinks = getimagelinks(productlink.split('?')[0])
    print(f'Found image links: {len(imagelinks)}')
    if not imagelinks:
        print(f'image links not found, skipping {imagelinks=}')
    imagelinks = list(set([link.get('href') for link in imagelinks]))
    for i, link in enumerate(imagelinks):
        print(f"Saving [{i+1} out of {len(imagelinks)}]", end='\r')
        getimagecontent(i, link, productcode)
    print(f"Estimated time to completion: {(((perf_counter()-start)/(offset-2))*(length-(offset-2)))//60}")
f.close()