# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.spiders import CrawlSpider, Rule 
from scrapy.selector import Selector
from craigslistscraper.items import CraigslistscraperItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

keys = ['marketing', 'journalism', 'journalist', 'copywriting', 'communications', 'copywriter']

class JobsFinder(CrawlSpider):
    name = "jobsfinder"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://sfbay.craigslist.org/search/jjj"]


    def parse(self, response):
        item = CraigslistscraperItem()
        hxs = Selector(response)
        if any(key in response.body for key in keys):
            
            item['name'] = hxs.xpath('//span[@class="pl"]')
            item['url'] = response.url
            item['post_body'] = hxs.xpath("//section[@class='body']")
            yield item  