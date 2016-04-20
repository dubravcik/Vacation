from scrapy import Spider
from bs4 import BeautifulSoup
import datetime
import json
from ..items import VacationItem


class VacationEasySpider(Spider):
    name = 'vacation_easy'
    start_urls = ["http://hotel.invia.cz/direct/tour_detail/ajax-term-select-form-terms/?formData[d_start_from]=&formData[d_end_to]=&formData[c_price_int]=-1&formData[nl_hotel_id]=52988&formData[nl_tour_id]=&nl_page=1&sortField=&sortOrder="]

    def parse(self, response):

        body = json.loads(response.body).get('terms')
        soup = BeautifulSoup(body, 'html.parser')
        rows = soup.find_all('th')
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
            now = datetime.datetime.now()
            urlCrawled = response.url

            vacation = VacationItem()
            vacation['url'] = linkE
            vacation['createdAt'] = now
            vacation['locationFrom'] = locationFromE
            vacation['term'] = termE
            vacation['food'] = foodE
            vacation['days'] = daysE
            vacation['price'] = priceE
            vacation['urlCrawled'] = urlCrawled

            yield vacation