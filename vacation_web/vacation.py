__author__ = 'michal.dubravcik'
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../vacation.db'
db = SQLAlchemy(app)




if __name__ == '__main__':
    db.create_all()
    app.run(port=80)
