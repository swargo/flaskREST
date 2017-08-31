from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from pymongo import MongoClient

engine = create_engine('sqlite:///tutorial.db', echo=True)
metadata = MetaData(bind=engine)
allUsers = Table('users', metadata, autoload=True)
connection = MongoClient("mongodb://user:password@ds137882.mlab.com:37882/blueberry-muffins")
db = connection['blueberry-muffins']
collection = db.users
# users = {'sophie': 'wargo'}

# id = collection.insert_one(users).inserted_id

app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"


@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/register', methods=['POST'])
def do_admin_register():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    con = engine.connect()
    con.execute(allUsers.insert(), name=POST_USERNAME, password=POST_PASSWORD)

    return home()

@app.route('/loginmanager', methods=['GET', 'POST'])
def getPassword():
    if request.method=='POST':
        websiteName = request.form.get('website')
        id = request.form.get('userId')
        url = request.form.get('url')
        passw = request.form.get('password')
        notes = request.form.get('notes')
        loginInfo = { websiteName: { "websiteName": websiteName, "website": url, "password": passw, "infoNotes": notes, "userId": id }}
        collection.insert_one(loginInfo)
        return loginInfo
    elif request.method == 'GET':
        pws = ""
        cursor = collection.find({})
        for document in cursor:
            pws = pws + str(document)
            print(str(document))
        return pws


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=4000)