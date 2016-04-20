from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.crawler.spiders.vacation_easy import VacationEasySpider
from twisted.internet import reactor


spider = VacationEasySpider()
settings = get_project_settings()
crawler = CrawlerProcess(settings)

crawler.crawl(spider)
crawler.start() # the script will block here