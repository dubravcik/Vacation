from web import db

class Vacation(db.Model):
    url = db.Column(db.String(500), primary_key=True)
    createdAt = db.Column(db.String(50), primary_key=True)
    term = db.Column(db.String(50))
    locationFrom = db.Column(db.String(50))
    food = db.Column(db.String(50))
    urlCrawled = db.Column(db.String(500))
    days = db.Column(db.String(50))
    price = db.Column(db.String(50))

    def __init__(self, url, createdAt, term, locationFrom, food, days, price, urlCrawled):
        self.url = url
        self.createdAt = createdAt
        self.term = term
        self.locationFrom = locationFrom
        self.food = food
        self.days = days
        self.price = price
        self.urlCrawled = urlCrawled

    def __repr__(self):
        return 'Vacation ', self.createdAt, self.url

class Hotel(db.Model):
    url = db.Column(db.String(500), primary_key=True)
    id = db.Column(db.Integer)

    def __init__(self,url):
        self.url = url
    def __repr__(self):
        return 'Hotel', self.id