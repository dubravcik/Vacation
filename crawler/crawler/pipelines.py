import sys,os
sys.path.append(os.path.abspath('../'))
from web.models import Vacation
from web import db


class VacationCrawlerPipeline(object):
    def process_item(self, item, spider):
        vacation = Vacation(item['url'], item['createdAt'], item['term'], item['locationFrom'], item['food'], item['days'], item['price'], item['urlCrawled'])
        db.session.add(vacation)
        db.session.commit()
        return item
