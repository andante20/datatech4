# -*- coding: utf-8 -*-

import datetime, time
import json 
import re
from urllib.parse import urlencode
from urllib import parse

import logging
import scrapy
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser

from scrapy.conf import settings
from crawler.items import MeagakItem

class WooriSpider(scrapy.Spider):
    name = 'woori'
    
    bubwon = {'0101':'서울중앙지방법원',
        '0201':'서울동부지방법원',
        '0301':'서울서버지방법원',
        '0401':'서울남부지방법원',
        '0501':'서울북부지방법원',
        '0601':'의정부지방법원',
        '0602':'고양지원',
        '0701':'인천지방법원',
        '0702':'부천지원',
        '0801':'수원지방법원',
        '0802':'성남지원',
        '0803':'여주지원',
        '0804':'평택지원',
        '0805':'안산지원',
        '0806':'안양지원',
        '1101':'춘천지방법원',
        '1103':'강릉지원',
        '1102':'원주지원',
        '1104':'속초지원',
        '1105':'영월지원',
        '1001':'청주지방법원',
        '1002':'충주지원',
        '1003':'제천지원',
        '1004':'영동지원',
        '0901':'대전지방법원',
        '0905':'홍성지원',
        '0906':'논산지원',
        '0902':'천안지원',
        '0903':'공주지원',
        '0904':'서산지원',
        '1501':'대구지방법원',
        '1508':'안동지원',
        '1503':'경주지원',
        '1504':'김천지원',
        '1505':'상주지원',
        '1506':'의성지원',
        '1507':'영덕지원',
        '1509':'포항지원',
        '1502':'대구서부지원',
        '1201':'부산지방법원',
        '1202':'부산동부지원',
        '1203':'부산서부지원',
        '1301':'울산지방법원',
        '1401':'창원지방법원',
        '1406':'마산지원',
        '1405':'진주지원',
        '1402':'통영지원',
        '1404':'밀양지원',
        '1403':'거창지원',
        '1601':'광주지방법원',
        '1602':'목포지원',
        '1605':'장흥지원',
        '1603':'순천지원',
        '1604':'해남지원',
        '1701':'전주지방법원',
        '1703':'군산지원',
        '1704':'정읍지원',
        '1702':'남원지원',
        '1801':'제주지방법원'}

    bubwon_gae = {'0101': list(range(1,13))+[21],
        '0201': list(range(1,9)),
        '0301': list(range(1,19)),
        '0401': list(range(1,12)),
        '0501': list(range(1,12))+[21,32,42,51],
        '0601': list(range(0,18)),
        '0602': list(range(0,14)),
        '0701': list(range(1,32)),
        '0702': list(range(1,11)),
        '0801': list(range(1,24)),
        '0802': list(range(1,9)),
        '0803': list(range(1,7)),
        '0804': list(range(1,7)),
        '0805': list(range(1,14)),
        '0806': list(range(1,6)),
        '1101': list(range(1,5)),
        '1103': list(range(1,8)),
        '1102': list(range(1,5)),
        '1104': list(range(1,3)),
        '1105': list(range(1,5)) ,
        '1001': list(range(1,9)),
        '1002': list(range(1,5)) ,
        '1003': list(range(1,3)) ,
        '1004': list(range(1,3)),
        '0901': list(range(0,11)),
        '0905': list(range(1,7)),
        '0906': list(range(1,4)),
        '0902': list(range(1,8)),
        '0903': list(range(0,4)),
        '0904': list(range(1,7)),
        '1501': list(range(1,20)),
        '1508': list(range(1,4)),
        '1503': list(range(1,5)),
        '1504': list(range(0,5)),
        '1505': list(range(1,3)),
        '1506': list(range(1,3)),
        '1507': list(range(1,3)),
        '1509': list(range(1,4)),
        '1502': list(range(1,6)),
        '1201': list(range(0,20)),
        '1202': list(range(0,10)),
        '1203': list(range(0,6)),
        '1301': list(range(0,10)),
        '1401': list(range(0,12)),
        '1406': list(range(0,5)),
        '1405': list(range(1,6)),
        '1402': list(range(0,6)),
        '1404': list(range(1,4)),
        '1403': list(range(1,3)),
        '1601': list(range(0,28)),
        '1602': list(range(0,10)),
        '1605': list(range(1,3)),
        '1603': list(range(1,20)),
        '1604': list(range(1,7)),
        '1701': list(range(1,10)),
        '1703': list(range(1,8)),
        '1704': list(range(1,9)),
        '1702': list(range(1,3)),
        '1801': list(range(1,7))}

    base_url = "http://www.j123.co.kr/search01/auction_Result.asp"
    detail_url = "http://www.j123.co.kr/common01/mulgun_detail_popup.asp"

    def create_url(self, query_string):
        return self.base_url + '?' + urlencode(query_string)
    
    def start_requests(self):
        start = settings.get('START', datetime.date.today().strftime('%Y%m%d'))

        for bubwon_idx in self.bubwon.keys():
            for bubwon_gae_idx in self.bubwon_gae[bubwon_idx]:
                fd = {'resBubwon':'{}'.format(bubwon_idx),
                'resGae':'{0:02d}'.format(bubwon_gae_idx),
                'resSerStartdate':start,
                'resSerEnddate':'',
                'resChgPage':'1',
                'nowPge':'1',
                'resSort2':''}
                
                time.sleep(1)

                self.logger.info("REQUEST ==> {}-{}".format(self.bubwon[bubwon_idx], bubwon_gae_idx))
                r = scrapy.FormRequest(self.base_url, callback=self.parse_data, formdata=fd)
                r.meta['fd'] = fd

                yield r
           


    def parse_data(self, response):
        try:

            trs = response.xpath('//tr[contains(@bgcolor, "#ffffff")]')
            if len(trs) > 0:
                #open_in_browser(response)
                self.logger.info("fd = %s" % str(response.meta['fd']))
                for tr in trs:
                    trx = Selector(text=tr.extract())
                    row = trx.xpath('//td')

                    if len(row) == 0:
                        return

                    td2 =Selector(text=row[2].extract().replace('\r\n','').replace('\t',''))
                    itemType = td2.xpath('//b//text()').extract_first()

                    if itemType == '아파트':
                        auctionDate = re.findall('\d{4}\.\d{2}\.\d{2}', td2.extract())
                        td3 =Selector(text=row[3].extract().replace('\r\n','').replace('\t',''))
                        addr = td3.extract()[td3.extract().index('<br>')+4:td3.extract().index('<!--')]
                        auctionLoc = re.findall('>(\S*계)', td3.extract())
                        
                        id = re.findall("pop_detail\('(.+)',", td3.extract())[0]
                        
                        self.logger.info("{},{},{}".format(id, addr, itemType))
                    
                        fd2 = { "idcode":'{}'.format(id)}
                        yield scrapy.FormRequest(self.detail_url, callback=self.parse_detail, formdata=fd2)
                
                pages = re.findall("javascript:submit_chk\('(\d)'\);",response.text)
                if len(pages)>0:
                    self.logger.info("paging = %s" % str(pages))
                    #open_in_browser(response)

                    fd = response.meta['fd']
                    nowPage = int(str(fd['nowPge']))
                    linkPage = int(str(pages[-1]))

                    if linkPage > nowPage:
                        fd['nowPge'] = str(nowPage +1)
                        #self.logger.info("paging = %s -> %s" % (str(nowPage), fd['nowPge']))
                        r = scrapy.FormRequest(self.base_url, callback=self.parse_data, formdata=fd)
                        r.meta['fd'] = fd

                        yield r
                    
            else:
                self.logger.info("blank")

            
        except:
            open_in_browser(response)






    def parse_detail(self, response):
        #open_in_browser(response)
        values = response.xpath('//table[@id="jin_table"]//font[@color="red"]//text()')
        value = "0"

        if len(values) > 0:
            value = values[-1].extract()

        caNos = response.xpath('//table[@id="Table1"]//td[contains(@style,"font-size:18px")]//text()').extract()
        a1, a2, a3 = caNos
        a1 = a1.replace(' ','')
        a3 = a3.replace('\xa0','').replace(' ','')
        caNo = "{}{}{}".format(a1,a2,a3)

        data = MeagakItem()
        data['caNo'] = caNo
        data['value'] = int(value.replace(',',''))


        dts =  response.xpath('//table[@id="Table14"]//tr').extract()[1:]    
        if len(dts) > 0:
            refers = []
            for dt in dts:
                drx = Selector(text=dt)
                drxs = drx.xpath('//td//text()').extract()
                #self.logger.info(drxs)
                refers.append(
                {
                    'auctionInfo':'{} {}'.format(drxs[0].replace('\xa0',' '), drxs[1].replace('\xa0',' ')),
                    'auctionDate': drxs[2],
                    'value': int(drxs[3].replace(',','')),
                    'meagak': int(drxs[4].replace(',','')),
                    'count': int(drxs[5]),
                    'ratio': float(drxs[6].replace('%',''))
                })
            
            data['refers'] = refers



        yield data
