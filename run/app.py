from flask import Flask, jsonify, make_response, request, abort, render_template,session,redirect,url_for
from flask_cors import CORS, cross_origin
# import json
# import sqlite3
# import urllib.parse
import bcrypt
from time import gmtime, strftime
from pymongo import MongoClient
import random
from flask_mongoalchemy import MongoAlchemy
from flask_pymongo import PyMongo

# Object creation
app = Flask(__name__)
# app.config.from_object(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
# CORS(app)

# app.config['MONGOALCHEMY_DATABASE'] = 'app'
# app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://localhost:27017/'
app.config["MONGO_URI"] = 'mongodb://localhost:27017/cloud_native'

# Define connection to MongoDB
# username = urllib.parse.quote_plus('mongoadmin')
# password = urllib.parse.quote_plus('secret')
# connection = MongoClient("mongodb://%s:%s@0.0.0.0:27017/" % (username, password))
# connection = MongoClient('0.0.0.0:27017', username='mongoadmin', password='secret')
connection = MongoClient('127.0.0.1')
db = MongoAlchemy()

#mongo=PyMongo(app)

# connection.the_database.authenticate('mongoadmin','')

# Initialized MongoDB


def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'cloud_native' not in dbnames:
            db = connection.cloud_native.users
            db_tweets = connection.cloud_native.tweets
            db_api = connection.cloud_native.apirelease
            db.insert({
                "email": "testuser@test.local",
                "id": 33,
                "name": "Test user",
                "password": "12345",
                "username": "testuser"
            })

            db_tweets.insert({
                "body": "New tweets",
                "id": "18",
                "timestamp": "2017-03-11T06:39:40Z",
                "tweetedby": "testuser"
            })

            db_api.insert({
                "buildtime": "2017-01-01 10:00:00",
                "links": "/api/v1/users",
                "methods": "get, post, put, delete",
                "version": "v1"
            })

            db_api.insert({
                "buildtime": "2017-01-01 10:00:00",
                "links": "/api/v2/tweets",
                "methods": "get, post",
                "version": "v2"
            })
            print("Database Initialize completed!")
        else:
            print("Database already initialized")
    except:
        print("Database creation failed!")


def list_users():
    api_list = []
    db = connection.cloud_native.users
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'user_list': api_list})


def list_user(user_id):
    api_list = []
    db = connection.cloud_native.users
    for i in db.find({'id': user_id}):
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'user_list': api_list})
#    return jsonify(user)


def add_user(new_user):
    api_list = []
    #    print (new_user)
    db = connection.cloud_native.users
    user = db.find({'$or': [{"username": new_user['username']}, {"email": new_user['email']}]})
    for i in user:
        # print (str(i))
        api_list.append(str(i))
        # print(api_list)
    if api_list == []:
        print(new_user)
        db.insert(new_user)
        return "Success"
    else:
        abort(409)


def del_user(del_user):
    db = connection.cloud_native.users
    api_list = []
    for i in db.find({'username':del_user}):
        api_list.append(str(i))
        if api_list == []:
            abort(404)
        else:
            db.remove({"username":del_user})
            return "Success"
    return jsonify({'delete user': del_user})


def upd_user(user):
    api_list = []
    print(user)
    db_user = connection.cloud.native.users
    users = db_user.find({"id": user['id']})
    for i in users:
        api_list.append(str(i))
        if api_list == []:
            abort(409)
    else:
        db_user.update_one({'id': user['id']}, {'$set': user}, upsert=False)
    return "Success"


# api/v2
def list_tweets():
    api_list=[]
    db = connection.cloud_native.tweets
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'tweets_list': api_list})


def add_tweet(new_tweets):
    api_list=[]
    print (new_tweets)
    db_user = connection.cloud_native.users
    db_tweet = connection.cloud_native.tweets
    user = db_user.find({"username": new_tweets['username']})
    for i in user:
        api_list.append(str(i))
        if api_list == []:
            abort(404)
        else:
            db_tweet.insert_one(new_tweets)
        return "Success"


def list_tweet(user_id):
    db =connection.cloud_native.tweets
    api_list = []
    tweet = db.find({'id':user_id})
    for i in tweet:
        api_list.append(str(i))
        if api_list == []:
            abort(404)
    return jsonify({'tweet': api_list})

    return jsonify(user)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html', session=session['username'])

@app.route('/index')
def index():
    return render_template('index.html')


@app.route("/api/v1/info")
def home_index():
    api_list = []
    db = connection.cloud_native.apirelease
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'api_version': api_list}), 200


@app.route('/login', methods=['POST'])
def do_admin_login():
#    users = mongo.db.users
    users = connection.cloud_native.users
    api_list = []
    login_user = users.find({'username': request.form['username']})
    for i in login_user:
        api_list.append(i)
        print ("login user: ", api_list)
        if api_list !=[]:
            # print(api_list[0]['password'].decode('UTF-8'))
            if api_list[0]['password'] ==bcrypt.hashpw(request.form['password'].encode('utf-8'), api_list[0]['password']):
            # if api_list[0]['password'] == bcrypt.hashpw(request.form['password'].encode('utf-8'),
            #                                                            api_list[0]['password']):
                session['logged_in'] = api_list[0]['username']
                return redirect(url_for('index'))
        return "Invalid Authentication"
    return "Invalid User"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
       # users = mongo.db.users
        users = connection.cloud_native.users
        api_list=[]
        existing_user = users.find({'$or':[{"username":request.form['username']} ,{"email":request.form['email']}]})
        for i in existing_user:
            # print (str(i))
            api_list.append(str(i))

        # print (api_list)
        if api_list == []:
            users.insert({
            "email": request.form['email'],
            "id": random.randint(1,1000),
            "name": request.form['name'],
            "password": bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt()),
            "username": request.form['username']
            })
            session['username'] = request.form['username']
            return redirect(url_for('home'))

        return 'That user already exists'
    else :
        return render_template('signup.html')


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name', ""),
        'password': request.json['password'],
        'id': random.randint(1, 1000)
    }
    #    print(str(user))
    return jsonify({'status': add_user(user)}), 201


@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = request.json['username']
    return jsonify({'status': del_user(user)}), 200


@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
        abort(400)
    user['id'] = user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print(user)
    return jsonify({'status': upd_user(user)}), 200


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method=='POST':
        users = mongo.db.users
        api_list=[]
        existing_users = users.find({"username":session['username']})
        for i in existing_users:
            # print (str(i))
            api_list.append(str(i))
        user = {}
        print (api_list)
        if api_list != []:
            print (request.form['email'])
            user['email']=request.form['email']
            user['name']= request.form['name']
            user['password']=request.form['pass']
            users.update({'username':session['username']},{'$set': user} )
        else:
            return 'User not found!'
        return redirect(url_for('index'))
    if request.method=='GET':
        users = mongo.db.users
        user=[]
        print (session['username'])
        existing_user = users.find({"username":session['username']})
        for i in existing_user:
            user.append(i)
        return render_template('profile.html', name=user[0]['name'], username=user[0]['username'], password=user[0]['password'], email=user[0]['email'])


# api/v2 route
@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()


@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet['username'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['created_at'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    print(user_tweet)
    return jsonify({'status': add_tweet(user_tweet)}), 200


@app.route('/api/v2/tweets/<int:user_id>', methods=['GET'])
def get_tweet(user_id):
    return list_tweet(user_id)


@app.route('/adduser')
def adduser():
    return render_template('adduser.html')


@app.route('/addtweets')
def addtweetjs():
    return render_template('addtweets.html')


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)


@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == "__main__":
    create_mongodatabase()
    app.run(host='0.0.0.0', port=5000, debug=True)

