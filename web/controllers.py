from flask import Blueprint, request, session, g, redirect, url_for, abort, render_template, flash, Flask
from web.models import Vacation, Hotel
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from web import db

class HotelAdmin(ModelView):
    form_columns = ['id', 'url']

#web = Blueprint('web', __name__)
app = Flask(__name__)
admin = Admin(app, name='microblog', template_mode='bootstrap3')

class VacationModelView(ModelView):
    column_display_pk = True
    form_columns = ('url', 'createdAt', 'term', 'locationFrom', 'food', 'days', 'price', 'urlCrawled')
class HotelModelView(ModelView):
    column_display_pk = True
    form_columns = ('id', 'url')

admin.add_view(VacationModelView(Vacation, db.session))
admin.add_view(HotelModelView(Hotel, db.session))

@app.route('/')
def show_entries():
    vacations = Vacation.query.all()
    return render_template('show_entries.html', entries=vacations)
