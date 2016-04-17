from vacation_web import db

class Vacation(db.Model):
    url = db.Column(db.String(500), primary_key=True)
    datetime = db.Column(db.String(50), primary_key=True)

    def __init__(self, url, datetime):
        self.datetime = datetime
        self.url = url

    def __repr__(self):
        return 'Vacation ', self.datetime, self.url