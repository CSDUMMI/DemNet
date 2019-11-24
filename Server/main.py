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
messages = db.messages
"""
Layout of the users:
A User Document:
{
    'username' : Unique identification string
    'password' :
    'firstName' :
    'lastName' :
    'email' :
    'phone' :
    'messages' : ObjectIds of the Messages in  messages
}

Layout of the elections:
An Election Document:
{
    'participants' : Array of all usernames of those, who voted already
    'votes' : Array of all votes, without any association to a user
    'options' : Array of all the possibilities for a vote
    'deadline' : UTC Timestamp
}
Layout of messages:
A Message Document:
{
    'type' : 'Type of the Message' - Currently only 'text'
    'content' : 'Content of the Message'
    'title' : Title
    'author' : 'Username of the author of the message'
    'recipient' : Username of the user, to receive the message.
}
All messages are public!
"""
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
         'phone'     : phone,
         'messages'  : [messages.find_one({ 'title' : 'Welcome to DemNet', 'author' : 'devteam' })['_id']]
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

        election_id = ObjectId(election)
        election = elections.find_one({ '_id' : election })
        options = election.get('options')
        deadline = int(election.get('deadline'))

        if username in election.get('participants') or not (vote in options):
            return "AlreadyVoted"
        elif deadline < time.time():
            return "BallotClosed"
        else:
            elections.update_one({ '_id' : election_id },
                                 { '$push' :
                                    {
                                        'participants' : username,
                                        'votes': vote
                                    }
                                })
            return "Voted"
    else:
        return "NotVoted"

@app.route('/election')
def election():
    if( request.values.get('election') and elections.find_one({ '_id' : ObjectId(request.values.get('election')) }) ):

        election_id = ObjectId(request.values.get('election'))

        election = elections.find_one({ '_id' : ObjectId(election_id) })

        deadline = election.get('deadline')
        votes = election.get('votes')
        participants_count = len(election.get('participants'))
        options = election.get('options')

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
        and request.values.get('title')
        and users.get('recipient') ):

        title       = request.values['title']
        content     = request.values['posting']
        type        = request.values['type']
        author      = session['username']
        recipient   = request.values['recipient']

        message = {
            'title' : title,
            'content' : content,
            'type' : type,
            'author' : author,
            'recipient' : recipient
        }
        id = messages.insert_one(message).inserted_id
        users.update_one({ 'username' : recipient }, { '$push' : { 'messages' : id }})
        return "Posted"

@app.route('/messages')
def messages():
    if( session.get('username') ):
        return jsonify(users[session['username']]['messages'])
    else:
        return "NotLoggedIn"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
