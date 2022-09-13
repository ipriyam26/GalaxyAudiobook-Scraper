import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GalaxyBookSpider(CrawlSpider):
    name = 'galaxy_book'
    allowed_domains = ['goldenaudiobooks.com']
    start_urls = ['https://goldenaudiobooks.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # find the title
        title = response.css('.entry-title').extract_first()
        item = {
            'title': title,
            'url': response.url
        }

        yield item
