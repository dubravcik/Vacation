from datetime import datetime
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
    hotelId = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    hotel = db.relationship('Hotel', enable_typechecks=False)


    def __init__(self, url, term, locationFrom, food, days, price, urlCrawled, hotel):
        self.url = url
        self.createdAt = datetime.utcnow()
        self.term = term
        self.locationFrom = locationFrom
        self.food = food
        self.days = days
        self.price = price
        self.urlCrawled = urlCrawled
        self.hotel = hotel

    def __repr__(self):
        return 'Vacation '+str(self.createdAt) + str(self.url)

class Hotel(db.Model):
    url = db.Column(db.String(500))
    id = db.Column(db.Integer, primary_key=True)
    crawledAt = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
    vacation = db.relationship('Vacation')
    localityId = db.Column(db.Integer, db.ForeignKey('locality.id'))
    locality = db.relationship('Locality', enable_typechecks=False)

    def __init__(self, id, locality):
        self.id = id
        self.url = '-'
        self.locality = locality

    def __repr__(self):
        return 'Hotel ' + str(self.id)

class Locality(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    urlCrawled = db.Column(db.String(500))
    country = db.Column(db.String(500))
    locality = db.Column(db.String(500))
    crawledAt = db.Column(db.DateTime)
    hotel = db.relationship('Hotel')

    def __init__(self, country, locality):
        self.country = country
        self.locality = locality

    def __repr__(self):
        return 'Locality ' + str(self.country) + ' ' + str(self.locality)
