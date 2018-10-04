import re
import scrapy
from neaspider.items import ProvincepageItem, DampageItem
import time
import pprint
import json


class ProvincepageSpider(scrapy.Spider):
    """

    """
    name = 'PPS'
    allowed_domains = ["dam.com.cn"]
    dambaseURL = "http://www.dam.com.cn/damView/view.jsp?id="
    maxPage = 32
    start_urls = ["http://www.dam.com.cn/damView/getSdz.jsp?sfid="\
                  + str(num) for num in range(1, maxPage)]

    def parse(self, response):
        """

        :param response:
        :return:
        """
        #provinceItem = ProvincepageItem()
        province = response\
            .xpath('//td[@height="30" and @class="a5" and @align="center"]/text()').extract()
        if len(province) == 0:
            print('None page, pass')
        else:
            damType = response.xpath('//tr/td/div[@style]/text()').extract()

            for num, dtype in enumerate(damType):
                # select the name of dam and ID of dam
                xselectorName = '//tr[{}]/td[@style]/div/a[@href]/text()'.format(num+1)
                xselectorID = '//tr[{}]/td[@style]/div/a[@href]/@href'.format(num+1)

                # list contained dam's name
                damNameList = response.xpath(xselectorName).extract()
                # list contained dam's ID
                damIDList = response.xpath(xselectorID).re(r'\d\d\d\d')
                damLinkList = [self.dambaseURL+id for id in damIDList]
                #print(damNameList)
                #print(damIDList)
                #print(damLinkList)
                #time.sleep(40)
                # fill the contents
                for index, link in enumerate(damLinkList):
                    damItem = DampageItem()
                    provinceClean = re.match(r'【(.*?)】', province[0]).group(1)
                    damItem['Province'] = provinceClean
                    damItem['DamName'] = damNameList[index]
                    damItem['DamType'] = dtype
                    damItem['DamLink'] = link
                    damDesrequest = scrapy.Request(link, callback=self.parse_dam_description)
                    damDesrequest.meta['damItem'] = damItem

                    yield damDesrequest

    def parse_dam_description(self, response):
        """

        :param response:
        :return:
        """
        damItem = response.meta['damItem']
        #check page if is null page
        isNull = response.xpath('//tr/td[@class="nr3"]/p').extract()
        if len(isNull) == 0:
            print('dam description is null,skip')
            damItem['DamDescription'] = 'No description'
        else:
            damItem['DamDescription'] = response.xpath('//tr/td[@class="nr3"]').extract()[0]

        return damItem


#if __name__ == '__main__':
    #p = ProvincepageSpider()
    #print(p.start_urls)
