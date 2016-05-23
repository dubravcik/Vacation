import logging
from scraper.scraper import HotelScraper
from web import db

# Log to file
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(filename='log/scraper.log',level=logging.DEBUG, format=FORMAT)

# Log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)


hotel = HotelScraper.query.get(52988)
hotel.scrap()
hotel.setCrawledNow()
db.session.commit()