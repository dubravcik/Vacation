import json
from bs4 import BeautifulSoup
import datetime
import requests
from web.models import Vacation, Hotel
from web import db
import logging
from sqlalchemy.orm import mapper



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

class HotelScraper(Hotel):
    def __init__(self, id):
        super(HotelScraper, self).__init__(id)
        logger.info("Hotel created")

    def setCrawledNow(self):
        self.crawledAt = datetime.datetime.utcnow()
        logger.info(str(self.id) + " set date crawled now")

    def getUrl(self, page):
        hotel = self.id
        url = "http://hotel.invia.cz/direct/tour_detail/ajax-term-select-form-terms/?formData[d_start_from]=&formData[d_end_to]=&formData[c_price_int]=-1&formData[nl_hotel_id]="+str(hotel)+"&formData[nl_tour_id]=&nl_page="+str(page)+"&sortField=&sortOrder="
        return url

    def scrap(self):

        urls = UniqueDict()
        urls[1] = ''
        url = urls.getEmpty()

        if(self.crawledAt > datetime.datetime.utcnow() - datetime.timedelta(minutes=1)):
            logger.info( self.__repr__() + " already crawled in previous day")
        else:
            while url <> None:
                print "Urls status: ", urls
                print "Percentage done: {:.0%}".format(1 - (sum(urls[u] == '' for u in urls) / float(len(urls))))
                response = requests.get(self.getUrl(url))
                if response.status_code <> 200:
                    print "Scrapping failed"
                    logger.error("Failed scrapping: %s", url)
                else:
                    urls.setDone(url)
                    body = json.loads(response.text).get('terms')
                    paginator = json.loads(response.text).get('paginator')
                    logger.info("Scraped OK - %s",url)
                    bodySoup = BeautifulSoup(body, 'html.parser')
                    paginatorSoup = BeautifulSoup(paginator, 'html.parser')
                    rows = bodySoup.find_all('th')
                    pages = paginatorSoup.find_all('a')
                    for page in pages:
                        urls.addEmpty(page.get('data-page'))
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
                        logger.info("Data committed " + str(url))
                url = urls.getEmpty()
