import logging
from scraper.scraper import HotelScraper
from web import db
from sqlalchemy.sql import func

# Log to file
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(filename='log/scraper.log',level=logging.DEBUG, format=FORMAT)

# Log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)


ver = 2

if ver ==1:
    while True:
        hotel = HotelScraper.query.order_by(func.random()).first()
        hotel.scrap()
        hotel.setCrawledNow()
        db.session.commit()
elif ver == 2:
    countProcessed = 0
    hotels = HotelScraper.query.all()
    for hotel in hotels:    
        hotel.scrap()
        db.session.commit()
        countProcessed += 1
        print "Hotel percentage done: {:.0%}".format(countProcessed/float(len(hotels)))
elif ver == 3:
    hotel = HotelScraper.query.get(103523)
    hotel.scrap(True)
    hotel.setScrapedNow()


