from web.models import Vacation
from web import db
vacation = Vacation("xfggf", "y")
db.session.add(vacation)
db.session.commit()