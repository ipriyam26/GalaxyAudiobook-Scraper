
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GalaxyBookSpider(CrawlSpider):
    name = 'galaxy_book'
    allowed_domains = ['goldenaudiobooks.com']
    start_urls = ['https://goldenaudiobooks.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/*'), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=r'category/'), follow=True),
        Rule(LinkExtractor(allow=r'category/*'),  follow=True),
    )

    def parse_item(self, response):
        title = response.css('.entry-title::text').extract_first()
        image = response.css(".entry-content").re(
            "https:\/\/goldenaudiobook.b-cdn.net\/wp-content\/uploads\/[0-9]{4}\/[0-9]{2}\/\S*\.jpg")
        if image:
            image = image[0]
        audios = list(set(response.css(
            ".entry-content").re("https:\/\/ipaudio.club\/wp-content\/uploads\/\S*mp3\?_=[0-9]+")))
        author = response.css(".tags-links a").css("::text").get(default="Unknown")
        tags = response.css("#main .single").css("::text").getall()
        
        yield {'title': title, 'url': response.url, 'image': image, 'audios': audios, 'author': author,'tags': tags }
