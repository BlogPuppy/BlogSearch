import scrapy
from tutorial.items import BlogItem

class DmozSpider(scrapy.Spider):
    name="dmoz"
    #allowed_domains=["dmoz.org"]
    start_urls=[
        "http://qianjiye.de/categories/",
    ]

    def parse(self,response):
        for href in response.css(".post li.listing-item > a::attr('href')"):
            url=response.urljoin(href.extract())
            print url
            yield scrapy.Request(url,callback=self.parse_dir_contents)

    def parse_dir_contents(self,response):
        item=BlogItem()
        item['title']=response.css("#main").xpath("//header/h1/text()").extract()
        item['url']=response.url
        item['date']=response.css(".meta .time > time::attr('datetime')").extract()
        content=""
        for para in response.css(".post").xpath("p/text()").extract():
            content+=para
        item['content']=content
        yield item
