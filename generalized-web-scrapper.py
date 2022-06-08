from gc import callbacks
import rule
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

#which items from the urls do you wish to find? 
class itemstofind(Item):
    title = Field ()
    price  = Field ()
    description = Field ()

class crawler(CrawlSpider):
    name ='whatever name you want to use'
    
    # this settings prevent some blockage from the sites 
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7',
        'CLOSESPIDER_PAGECOUNT': 20,
    }
    delay = 1

    #narrow the search field to optimize the crawling and avoid ads 
    allowed_domains = ['graphics-card.whichever-site-you-want-to-scalp.com','ssd.whichever-site-you-want-to-scalp.com']
    
    #where do we start?
    start_urls = ['whichever-site-you-want-to-scalp.com']
    
    #we use rules as to determine where to stop looking. 
    #this example finds urls using the first rule and continues searching, 
    #but ends crawling (callback) when the second rule is met.
    rules = (
        #pages
        Rule(
            LinkExtractor(
                allow=r'whichever pattern you found in the url, usualy page=int'
                ), follow=True
        ),
        #products
        Rule(
            LinkExtractor(
                allow=r'whichever pattern you found in the url, usualy item=#itemUUID'
                ), follow=True, callback='items_parser'
        ),
    )

    #this helps deleting unnecessary text
    def textcleanse(self,text):
        newtext = text.replace('text-to-replace','replacement')
    
    #parsing the found urls. the first add_xpath parameter is the item to find
    #while the second one filters on the html tags as text
    def items_parser(self, response):
        item = ItemLoader(itemstofind(), response, MapCompose(self.textcleanse))
        item.add_xpath('title','//tag-to-filter/text()')
        item.add_xpath('price','')
        item.add_xpath('description','')

        yield item.load_item()

