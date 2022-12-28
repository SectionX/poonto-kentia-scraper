import requests
from bs4 import BeautifulSoup as BS
import os
import openpyxl as xl
from time import sleep, perf_counter
import pprint as pp
import re
from multiprocessing import Pool




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

# wb = xl.load_workbook('kentia-2022-12-27-diff(2)-v2.xlsx')
# sheet = wb['CMSInput']

# length = 1
# while sheet['b'+str(length+1)].value:
#     length += 1

# start = perf_counter()

def app(item):
    url = 'https://www.kentia.gr/el/product-search?search='
    f = open('log_failed.txt', 'a')
    productcode = item
    print(f'Downloading item {item}')
    if not productcode:
        return
    productlink = getproductlink(url, productcode)
    if not productlink:
        print(f'product link not found, logging {productcode=}')
        f.write(f"{productcode}'\n'")
        return
    imagelinks = getimagelinks(productlink.split('?')[0])
    print(f'Found image links: {len(imagelinks)}')
    if not imagelinks:
        print(f'image links not found, skipping {imagelinks=}')
    imagelinks = list(set([link.get('href') for link in imagelinks]))
    for i, link in enumerate(imagelinks):
        print(f"Saving [{i+1} out of {len(imagelinks)}]", end='\r')
        getimagecontent(i, link, productcode)
    # print(f"Estimated time to completion: {(((perf_counter()-start)/(offset-2))*(length-(offset-2)))//60}")
    f.close()


def import_product_codes() -> list[str]:

    #xlsx filename input & sanitation
    files = os.listdir()
    print("Select a file by number")
    for i, file in enumerate(files):
        if not re.search(".*\.xls.", file):
            files[i] = ""
    
    while "" in files:
        files.pop(files.index(""))
    
    for i, file in enumerate(files):
        print(f"{i} - {file}")
    flag = True
    while flag:
        try:
            filename = files[int(input("> "))]
            flag = False
        except Exception as e:
            if e != KeyboardInterrupt:
                print(f"Input must be a number between 0 and {len(files)-1}")
            else: break
    
    #creating a list of codes
    codes = []
    wb = xl.load_workbook(filename)
    sheet = wb['CMSInput']
    offset = 2
    while sheet[f'b{offset}'].value:
        codes.append(sheet[f'b{offset}'].value)
        offset += 1

    return codes


def main(threads=4):
    products = import_product_codes()
    with Pool(threads) as pool:
        pool.map(app, products)


if __name__ == "__main__":
    main()