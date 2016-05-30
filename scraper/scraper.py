import json
import datetime
import logging

from bs4 import BeautifulSoup
import requests

from web import db
from web.models import Locality, Hotel, Vacation

logger = logging.getLogger(__name__)

class UniqueDict(dict):
    def getEmpty(self):
        try:
            return self.keys()[self.values().index('')]
        except ValueError:
            return None

    def addEmpty(self, key):
        if key not in self.keys():
            self.__setitem__(key, '')

    def setDone(self, key):
        self.__setitem__(key, 'x')

class LocalityScraper(Locality):

    def setCrawledNow(self):
        self.crawledAt = datetime.datetime.utcnow()
        logger.info(str(self.id) + " set date crawled now")

    def getUrl(self, page):
        return 'http://last-minute.invia.cz/direct/tour_search/ajax-next-boxes/?nl_country_id%5B%5D='+str(self.country)+'&nl_locality_id%5B%5D='+str(self.locality)+"&page="+str(page)

    def scrap(self):
        pages = UniqueDict()
        pages[1] = ''
        page = pages.getEmpty()
        while page <> None:
            url = self.getUrl(page)
            response = requests.get(url) #28, 291
            logger.info("Fetching locality of url "+str(url)+" page "+str(page))
            if response.status_code <> 200:
                logger.error("Failed %s", self)
            else:
                try:
                    self.setCrawledNow()
                    pages.setDone(page)
                    body = (json.loads(response.text)).get('boxes_html')
                    bodySoup = BeautifulSoup(body, 'html.parser')
                    lis = bodySoup.find_all('li', attrs={"class":"item"})
                    pagesScrap = bodySoup.find('span', class_="pages").find_all('a')
                    for pageScrap in pagesScrap:
                        pages.addEmpty(int(pageScrap.get('data-page')))
                    for li in lis:
                        hotelId = json.loads(li.get('data-ua')).get('name').split(' ',1)[0]

                        if hotelId.isdigit():
                            logger.info("Hotel "+str(hotelId)+" found")
                            hotel = Hotel(hotelId, self)
                            db.session.merge(hotel)
                            db.session.commit()
                        else:
                            logger.warn("Invalid hotel found: "+hotelId)
                except Exception as e:
                    logger.exception("Exception in parsing %s %s", e, body)

            page = pages.getEmpty()


class HotelScraper(Hotel):
    def __init__(self, id):
        self.setCrawledNow()
        super(HotelScraper, self).__init__(id)
        logger.info("Hotel created")

    def setCrawledNow(self):
        self.crawledAt = datetime.datetime.utcnow()
        logger.info(str(self.id) + " set date crawled now")

    def getUrl(self, page):
        hotel = self.id
        url = "http://hotel.invia.cz/direct/tour_detail/ajax-term-select-form-terms/?formData[d_start_from]=&formData[d_end_to]=&formData[c_price_int]=-1&formData[nl_hotel_id]="+str(hotel)+"&formData[nl_tour_id]=&nl_page="+str(page)+"&sortField=&sortOrder="
        return url

    def isScrapedToday(self):
        if self.crawledAt == None:
            return False
        return self.crawledAt > datetime.datetime.utcnow() - datetime.timedelta(hours=12)

    def scrap(self, ignoreConditions=False):

        pages = UniqueDict()
        pages[1] = ''
        page = pages.getEmpty()

        if(self.isScrapedToday() and  not (ignoreConditions)):
            logger.info( self.__repr__() + " already crawled today")
        else:
            while page <> None:
                response = None
                try:
                    print "Urls status: ", pages
                    print "Percentage done: {:.0%}".format(1 - (sum(pages[u] == '' for u in pages) / float(len(pages))))
                    url = self.getUrl(page)
                    logger.info("Scrapping "+str(url))
                    response = requests.get(url)
                    if response.status_code <> 200:
                        print "Scrapping failed"
                        logger.error("Failed scrapping: %s", page)
                    else:
                        pages.setDone(page)
                        body = json.loads(response.text).get('terms')
                        paginator = json.loads(response.text).get('paginator')
                        logger.info("Scraped OK - %s",page)
                        bodySoup = BeautifulSoup(body, 'html.parser')
                        paginatorSoup = BeautifulSoup(paginator, 'html.parser')
                        rows = bodySoup.find_all('th')
                        pagesCrawl = paginatorSoup.find_all('a')
                        for pageCrawl in pagesCrawl:
                            pages.addEmpty(pageCrawl.get('data-page'))
                        for row in rows:
                            termE = row.a.get_text().strip()
                            linkE = row.a.get('href').strip()
                            days = row.find_next_sibling()
                            daysE = days.get_text().strip()
                            food = days.find_next_sibling()
                            foodE = food.get_text().strip()
                            locationFrom = food.find_next_sibling()
                            locationFromE = locationFrom.get_text().strip()
                            price = locationFrom.find_next_sibling()
                            priceE = price.get_text().strip()
                            urlCrawled = response.url
                            vacation = Vacation(linkE, termE, locationFromE, foodE, daysE, priceE, urlCrawled, self)
                            db.session.add(vacation)
                            db.session.commit()
                            logger.info("Data committed " + str(vacation))
                    page = pages.getEmpty()
                except Exception as e:
                    logger.exception("In scraping exception %s, this was response: %s", e, response)
            self.setCrawledNow()
            db.session.commit()