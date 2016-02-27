# Please refer to the documentation for information on how to create and manage

# your spiders.

import scrapy

from scrapy.spiders import CrawlSpider, Rule

from scrapy.selector import Selector

from craigslistscraper.items import CraigslistscraperItem

from scrapy.linkextractors import LinkExtractor

import urlparse

import string

from datetime import date, timedelta


#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor



keys = ['marketing', 'journalism', 'journalist', 'copywriting', 'communications', 'copywriter', 'content', 'writer']

yesterday = date.today() - timedelta(days=1)

targetdepth = 1


linkextractors = [



]


#selectorConfig only has hub pages, not end pages
selectorConfig = {

   0 : [['//div[@id="jjj"]/h4/a', 1]],
   1 : [
        
        ['//a[@class="hdrlnk"]', 2], #job description links 
        
        ['//span[@class="buttons"]/a[@class="button next"]', 1] # next page links
        
        ]
    
      

}

seed_urls = ["http://sfbay.craigslist.org"]

url_to_type = {
               url : 0 for url in seed_urls
               
               }

class JobsFinder(CrawlSpider):

    name = "jobsfinder"

    allowed_domains = ["craigslist.org"]

    start_urls = seed_urls
    # Rule = 


            
            
        
    def parse(self, response):

        def parsejobpage(response):
            postingurl=response.url
            postingtitle = response.selector.xpath('//span[@class="postingtitletext"]/span[@id="titletextonly"]/text()').extract()[0]
            postingbody = ''.join(response.selector.xpath('//section[@id="postingbody"]//text()').extract()).encode('ascii', 'ignore')
            postingdate = 
            filename = filter(lambda x: x == ' ' or x.isalpha(), postingtitle)
            
            if postingdate > yesterday:
                if key in postingbody or postingtitle for key in keys:
                    with open("./jobpages/" + filename, "w") as output_file:
                        output_file.write(postingtitle + " " + postingurl + "\n" + postingbody)
                
        print response.meta, '\n', response
        
        url = response.url
        
        if not url in url_to_type:
            print url
            return
        
        current_type = url_to_type[url]
        if current_type == 2:
            parsejobpage(response)
            return
        if current_type not in selectorConfig:            
            with open('craigslist-jobs.txt', 'a') as output_file:
                output_file.write(response.body)
                return
         
        for pattern, page_type in selectorConfig[current_type]:
            anchors = response.selector.xpath(pattern)
            for anchor in anchors:    
                link = anchor.xpath('@href').extract()[0]
                name = anchor.xpath('text()').extract()
                name = name[0] if len(name) > 0 else ''
                link = urlparse.urljoin(response.url, link)
                url_to_type[link] = page_type
                print link 
                yield scrapy.Request(link, callback = self.parse)