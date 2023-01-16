import scrapy
import scrapy
import json
import os
import re
from urllib.parse import urljoin

import scrapy

class harrodsSpider(scrapy.Spider):
    name = 'harrods'
    sort_index = 4
    custom_settings = {
        "FEEDS": {
            os.path.join("scrapy_output", "harrods.csv"): {
                "format": "csv",
                "overwrite": True,
            }
        },
       
    }
    
    def __init__(self, *args, **kwargs):
        # setup google spreadsheet link
        json_file = os.path.join("inputs", "harrods_inputs.txt")
        with open(json_file, "r", encoding="utf-8") as file:
            config = json.loads(file.read())
        self.spreadsheet_link = config["spreadsheet_link"]

        super().__init__(*args, **kwargs)

    def start_requests(self):
        
        
     

        params = {
            'icid': 'megamenu_shop_women',
            'pageindex': '4',
        }
        links_file = os.path.join("links", "harrods.txt")
        with open(links_file, "r", encoding="utf-8") as links_file:
            start_urls = list(links_file.readlines())
      
        for url in start_urls:
            print(url)
            link=url
            url=link.replace('en-us/shopping/','api/commerce/v1/listing/')+'&pageindex=1'
            yield scrapy.Request(url=url, headers=headers,callback=self.parse_category_page)

         

    def parse_category_page(self, response):
        self.logger.info(f"Product category page sub page found {response.url}")
        

        
        jsonresponse = json.loads(response.text)
      


        
        counter=0
        while counter<len(jsonresponse['products']['entries']):
            productData=jsonresponse['products']['entries'][counter]
            sale=float(productData['price'])
            regularPrice=float(productData['priceWithoutDiscount'])
            brand=productData['brand']['name']
            slug=productData['slug']        
            productURL='https://www.harrods.com/en-us/shopping/'+slug
            title=productData['shortDescription']
            image=productData['images'][0]['url'].replace('_200','_1000')
            print(sale) 
            print(regularPrice)
            print(brand)
            print(productURL)
            print(image)
        

            difference=0
            try:
                difference=((regularPrice-sale)/regularPrice)*100
            except:
                difference=""
            print(difference)


            item = {}

            item["name"] = title
            item["brand"] = brand
            item["Sale Pirce"] =sale
            item["original price"] =regularPrice
            item["difference (%)"] =difference
            item["url"] = productURL
            item["image"] = image



            yield item
           

            counter=counter+1

        
        totalPages=jsonresponse['products']['totalPages']
        pageno=jsonresponse['products']['number']

        url=response.url.split('pageindex=')
        url=url[0]+'pageindex='+str(int(url[1])+1)
        print(url)
        
        if int(pageno)<int(totalPages):
            url=response.url.split('pageindex=')
            url=url[0]+'pageindex='+str(int(url[1])+1)
            print(url)
            yield scrapy.Request(url=url, headers=headers,callback=self.parse_category_page)
          
    
        
     

        