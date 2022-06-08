from gc import callbacks
import rule
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class article(Item):
    title = Field ()
    #price  = Field ()
    #description = Field ()

class melicrawler(CrawlSpider):
    name ='mercadolibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7',
        'CLOSESPIDER_PAGECOUNT': 23,
    }

    delay = 1
    allowed_domains = ['computacion.mercadolibre.com.ar','articulo.mercadolibre.com.ar', 'mercadolibre.com.ar', 'listado.mercadolibre.com.ar']
    start_urls = ['https://computacion.mercadolibre.com.ar/componentes-pc/']
    
    rules = (
        #pages
        Rule(
            LinkExtractor(
                allow=r'/_Desde_'
                ), follow=True
        ),
        #products
        Rule(
            LinkExtractor(
                allow=r'/MLA'
                ), follow=True, callback='items_parser'
        ),
    )

    def textcleanse(self,text):
        newtext = text.replace('\','').replace('\','').replace('\','').replace('\','').replace('\','').replace('\','')
    def items_parser(self, response):
        #sel =  Selector()
        item = ItemLoader(article(), response, MapCompose(self.textcleanse))
        item.add_xpath('title','//title/text()')
        #item.add_xpath('price','')
        #item.add_xpath('description','')

        yield item.load_item()

