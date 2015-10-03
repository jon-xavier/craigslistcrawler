# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.spiders import CrawlSpider, Rule 
from scrapy.selector import Selector, HtmlXPathSelector
from craigslistscraper.craigslistscraper.items import CraigslistscraperItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

keys = ['marketing', 'journalism', 'journalist', 'copywriting', 'communications', 'copywriter']

class JobsFinder(CrawlSpider):
    name = "jobsfinder"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://sfbay.craigslist.org/search/jjj"]

    rules = (
            (Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=(//span[@class='buttons']/a[@class='button next'],)), callback="parse_items", follow= True),
            )

    def parse_items(self, response):
        item = CraigslistscraperItem
        hxs = HtmlXPathSelector(response)
        if any(key in response.body for key in keys):
            
            item['name'] = hxs.xpath('//span[@class="pl"]')
            item['url'] = response.url
            item['postbody'] = hxs.xpath("//section[@class='body']")
            yield item 
        else pass       