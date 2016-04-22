import json
from bs4 import BeautifulSoup
import datetime
import requests
from web.models import Vacation
from web import db
import logging

logger = logging.getLogger(__name__)


url = "http://hotel.invia.cz/direct/tour_detail/ajax-term-select-form-terms/?formData[d_start_from]=&formData[d_end_to]=&formData[c_price_int]=-1&formData[nl_hotel_id]=52988&formData[nl_tour_id]=&nl_page=1&sortField=&sortOrder="
response = requests.get(url)
if response.status_code <> 200:
    print "Scrapping failed"
    logger.error("Failed scrapping")

else:
    body = json.loads(response.text).get('terms')
    logger.info("Scraped OK")
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

        vacation = Vacation(linkE, now, termE, locationFromE, foodE, daysE, priceE, urlCrawled)
        db.session.add(vacation)
        db.session.commit()
        print "Data committed"