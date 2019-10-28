from flask import Flask, request, session, jsonify
from election import count_votes
from Crypto.Hash import SHA256
import json, os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

users = json.load(open( 'users.json'))
elections = json.load( open('elections.json'))

def save():
    json.dump(users, open("users.json", "w+") )
    json.dump(elections, open("elections.json", "w+") )

@app.route('/login')
def login():
    # Logout automatically
    if request.values.get('username') and request.values.get('password'):
        hash = SHA256.new( request.values.get('password') ).hexdigest()
        username = request.values.get('username')

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
        and request.values.get('secondName')
        and not users.get( request.values.get('username'))
        ):

        username = request.values.get('username')
        firstName = request.values.get('firstName')
        secondName = request.values.get('secondName')
        hash = SHA256.new( request.values.get('password').encode('utf-8')).hexdigest()
        email = request.values.get('email')

        session['username'] = username # Login automatically
        users[username] = {
            "username" : username,
            "firstName" : firstName,
            "secondName" : secondName,
            "email" : email,
            "password" : hash
        }
        save()
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

        vote = request.values.get('vote').split(';')
        election = request.values.get('election')
        username = session.get('username')

        if username in elections[election]['participants']:
            return "AlreadyVoted"
        else:
            elections[election]['participants'].append( username )
            elections[election]['votes'].append( vote )
            save()
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
