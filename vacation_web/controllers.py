from flask import Blueprint, request, session, g, redirect, url_for, abort, render_template, flash
from vacation_web.models import Vacation

web = Blueprint('web', __name__)

@web.route('/')
def show_entries():
    vacations = Vacation.query.all()
    return render_template('show_entries.html', entries=vacations)
