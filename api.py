from flask import Flask, render_template
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from wtforms import Form, StringField, SubmitField

app = Flask(__name__)
api = Api(app)

app.config['MONGO3_HOST'] = 'mongodb://admin:password@ds137882.mlab.com:37882/blueberry-muffins'
app.config['MONGO3_DBNAME'] = 'blueberry-muffins'
mongo3 = PyMongo(app, config_prefix='MONGO3')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def home_page():
    online_users = mongo3.db.users.find({'online': True})
    return render_template('index.html',
        online_users=online_users)

@app.route('/user/<username>')
def user_profile(username):
    user = mongo3.db.users.find_one_or_404({'_id': username})
    return render_template('user.html',
        user=user)