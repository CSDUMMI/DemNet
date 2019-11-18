from flask import Flask, request, session, jsonify
from election import count_votes
from Crypto.Hash import SHA256
import json, os
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# MongoDb connection
client = MongoClient()
db = client.demnet
users = db.users
elections = db.elections

@app.route('/login')
def login():
    # Logout automatically
    if request.values.get('username') and request.values.get('password'):
        hash = SHA256.new( request.values.get('password') ).hexdigest()
        username = request.values.get('username')

        user = users.find_one({ 'username' : username })
        if hash == users[username]['password']:
            session['username'] = username
            return 'LoggedIn'

    else:
        return 'NotLoggedIn'

@app.route('/register')
def register():

    if (
        request.values.get('username')
        and request.values.get('password')
        and request.values.get('email')
        and request.values.get('firstName')
        and request.values.get('lastName')
        and request.values.get('phone')
        and users.find_one({ 'username' : request.values.get('username') }) == None
        ):

        username = request.values.get('username')
        firstName = request.values.get('firstName')
        secondName = request.values.get('secondName')
        hash = SHA256.new( request.values.get('password').encode('utf-8')).hexdigest()
        email = request.values.get('email')
        phone = request.values.get('phone')

        session['username'] = username # Login automatically
        user = {
         'username'  : username,
         'password'  : hash,
         'email'     : email,
         'first_name': first_name,
         'last_name' : last_name,
         'phone'     : phone
        }
        users.insert_one(user)

        return "Registered"
    else:
        return "NotRegistered"

@app.route('/vote')
def vote():
    if (
        request.values.get('vote')
        and request.values.get('election')
        and session.get('username')
        ):

        vote = request.values.get('vote')
        election = request.values.get('election')
        username = session.get('username')

        election = elections.find_one({ '_id' : ObjectId(election) })

        if username in elections[election]['participants']:
            return "AlreadyVoted"
        else:
            elections[election]['participants'].append( username )
            elections[election]['votes'].append( vote )
            return "Voted"
    else:
        return "NotVoted"

@app.route('/election')
def election():
    if( request.values.get('election') and elections.get( request.values.get('election') )):

        election = request.values.get('election')

        deadline = elections[election]['deadline']
        participants = elections[election]['participants']
        votes = elections[election]['votes']
        options = elections[election]['options']
        participant_count = len(participants)


        if int(deadline) > time.time():
            return "BallotNotClosed"
        else:
            return jsonify( count_votes( votes, participants_count, options ) )
    else:
        return 'NotAnElection'

@app.route('/post')
def post():
    if ( request.values.get('posting')
        and request.values.get('type')
        and session.get('username')
        and request.values.get('recipient')
        and users.get('recipient') ):

        content     = request.values['posting']
        type        = request.values['type']
        author      = session['username']
        recipient   = request.values['recipient']

        users[recipient]['messages'].append({ "content" : content, "type" : type, "author" : author })
        if type == "image":
            img = request.files['uploaded_img']
            f.save( "/static" + secure_filename(f.filename) )

        return "Posted"

@app.route('/messages')
def messages():
    if( session.get('username') ):
        return jsonify(users[session['username']]['messages'])
    else:
        return "NotLoggedIn"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
