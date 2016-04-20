from scrapy.crawler import CrawlerProcess
from crawler.crawler.spiders.vacation_easy import VacationEasySpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(VacationEasySpider)
process.start()