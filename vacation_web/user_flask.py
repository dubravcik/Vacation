from sqlalchemy.orm import sessionmaker

__author__ = 'michal.dubravcik'
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from user import User
from base import engine

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def show_entries():
    print session.query(User).first()
    return "v"

if __name__ == '__main__':
    app.run(port=80)
