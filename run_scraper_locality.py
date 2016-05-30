
import logging

# Log to file
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(filename='log/scraper.log',level=logging.DEBUG, format=FORMAT)

# Log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

from scraper.scraper import LocalityScraper

locality = LocalityScraper.query.get(2)
locality.scrap()