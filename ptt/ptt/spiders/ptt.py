from ptt.items import PostItem
import scrapy
import time
from bs4 import BeautifulSoup

class PTTspider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html']
    
    def parse(self,response):
        for i in range(1,100):
            time.sleep(0.5)
            url = "https://www.ptt.cc/bbs/Gossiping/index" + str(39396 - i) + ".html"
            yield scrapy.Request(url,cookies={'over18':'1'},callback = self.parse_article)
            
    def parse_article(self,response):
        res = BeautifulSoup(response.body)
        titles = res.find_all('div','title')
        for l in titles:
            
            links = 'https://www.ptt.cc' + l.find('a')['href']
            
            meta = {'url':links}
            yield scrapy.Request(links,callback = self.parse_content,meta=meta)
            
    
    def parse_content(self,response):
        item = PostItem()
        try:
            item['author'] = response.css('span.article-meta-tag::text')[0].extract()
            item['url'] = response.meta['url']             #連結
            item['title'] = response.css('span.article-meta-value::text')[2].extract() #標題
            item['date'] = response.css('span.article-meta-value::text')[3].extract() #日期
            item['content'] = response.css('#main-content::text')[0].extract().replace('\n','') #文章內容
            yield item
        
        except IndexError:
            pass
        
        
        