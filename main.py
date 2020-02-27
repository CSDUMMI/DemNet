#!/usr/bin/env python3

# OWN MODULES
from Server import Elections, Patches, Users
# FLASK
from flask import Flask, request, render_template, session, redirect
# MONGODB
import pymongo
from pymongo import MongoClient
# PYCRYPTODOME
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
# UITILS
from typing import List
import json, os, datetime, random

app = Flask( __name__
           , static_url_path="/static"
           , static_folder="output/static"
           , template_folder="output")
app.secret_key = os.environ["SECRET_KEY"]

client              = MongoClient()
db                  = client.demnet
messages            = db.messages
users               = db.users
elections           = db.elections

# Errors
debug                       = os.environ.get("DEBUG")
errors = { "OK"                         : "0"
         , "error_for_unknown_reason"   : "1"
         , "error_but_not"              : "2"
         , "invalid_data"               : "3"
         , "invalid_context"            : "4"
         , "not_logged_in"              : "5"
         , "invalid_user"               : "6"
         , "already_registered"         : "7"
         , "no_user_with_that_name"     : "8"
         , "invalid_password"           : "9"
         , "already_voted"              : "A"
         }

errors = { key : errors[key] if not debug else key for key in errors }

class Error (Exception):
    def status(self):
        return errors[self.args[0]]


@app.route("/", methods=["GET"])
def index():
    try:
        messages_count      = 10
        sorted_messages     = list(messages.find({}))
        upload_time_cut     = max(sorted_messages,key=lambda m: m["upload_time"])["upload_time"] - messages_count
        sorted_messages     = list(filter(lambda m: m["upload_time"] >= upload_time_cut, sorted_messages))
        sorted_messages     = list(map( lambda m:       { "title" : m["body"]["title"]
                                                        , "hash" : m["hash"] }
                                                        , sorted_messages
                                    )
                                )
        response =  render_template ( "index.html"
                                    , messages  = sorted_messages
                                    , logged_in = session.get("username") != None
                                    )

    except Exception as e:
        raise e
    else:
        return response


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            username = request.values["username"]
            password = SHA256.new(request.values["password"].encode("utf-8")).hexdigest()

            user = users.find_one({ "username" : username })
            if user:
                if password in user["passwords"]:
                    session["username"] = username
                else:
                    raise Error("invalid_password")
            else:
                raise Invalid_Data("no_user_with_that_name")
            response            = redirect("/")

    except KeyError:
        return errors["invalid_data"]
    except Error as e:
        return e.status()
    except Exception as e:
        raise e
    else:
        return response


@app.route("/readings", methods=["GET"])
def readings():
    try:
        readings    = users.find_one({ "username" : session["username"] })["readings"]
        readings    = [messages.find_one({ "hash" : reading }) for reading in readings]
        readings    = [(reading["body"]["title"], reading["hash"]) for reading in readings]
        response    = render_template("readings-index.html", readings=readings)
    except KeyError:
        return errors["not_logged_in"]
    except Exception as e:
        raise e
    else:
        return response

@app.route("/writings", methods=["GET"])
def writings():
    try:
        writings    = users.find_one({ "username" : session["username"] })["writings"]
        writings    = [messages.find_one({ "hash" : writing }) for writing in writings]
        writings    = [(writing["body"]["title"],writing["hash"]) for writing in writings]
        response    = render_template("writings-index.html", writings=writings)
    except KeyError:
        return errors["not_logged_in"]
    except Exception as e:
        raise e
    else:
        return response

@app.route("/read/<reading_hash>", methods=["GET"])
def read(reading_hash):
    try:
        reading     = messages.find_one({ "hash" : reading_hash })
        if reading["draft"]:
            raise Error("invalid_context")
        else:
            response    = render_template("read.html", reading=reading)
    except Error as e:
        return e.status()
    except Exception as e:
        raise e
    else:
        return response

@app.route("/write", methods=["GET","POST"])
def write_new():
    try:
        if request.method =="GET":
            response    = render_template("write.html", writing={})
        else:
            title       = request.values["title"]
            content     = request.values["content"]
            author      = session["username"]
            user_author = users.find_one({ "username" : author })
            hash        = f"{author}#{str(random.randint(0,99999)).zfill(5)}" #temporary, while files is still changing
            message     =   { "body"    :   { "title"   : title
                                            , "content" : content
                                            }
                            , "from"    : author
                            , "hash"    : hash
                            , "draft"   : True
                            }

            messages.insert_one(message)
            response    = redirect(f"/write/{hash}")
    except KeyError:
        return errors["invalid_user"]
    except Error as e:
        return e.status()
    except Exception as e:
        raise e
    else:
        return response



@app.route("/write/<writing_hash>", methods=["GET", "POST"])
def write(writing_hash):
    try:
        if request.method == "GET":
            writing     = messages.find_one({ "hash" : writing_hash })

            if session["username"] == writing["author"]:
                response    = render_template("write.html", writing=writing)
            else:
                raise Error("invalid_user")
        else:
            hash                = request.values["hash"]
            message             = messages.find_one({"hash" : hash})
            message["title"]    = request.values["title"]
            message["content"]  = request.values["content"]
            publish             = request.values["publish"] == "1"

            if publish:
                message["hash"]     = SHA256.new(json.dumps(message).encode("utf-8")).hexdigest()
                message["draft"]    = not publish
                messages.replace_one({ "hash" : hash }, message)
            else:
                messages.update_one({ "hash" : hash }, message)

    except Error as e:
        return e.status()
    except KeyError:
        return errors["invalid_context"]
    else:
        return response

"""
# The three stage process of an election.
The last step of an election is clear, the vote.
But before that can happen two other steps have to prepare the vote.

0. Proposing the vote
Here a problem is explained.
This can be in form of a simple title
or a long study, containing reasoning,
technical details and a concret case for why this problem needs addressing.

1. Collecting options
After the problem has been detailed, everybody is free to create a solution
and propose it as an option.

2. Voting
Now every user is held to vote on the issue and select
the best solution to the problem.

The first stage can take as long as it wants.
One can research an issue for years and deliver an extremely
detailed proposal for the issue, but once it is detailed and
officially proposed, the solutions must be proposed over a one
month period.
It is  thus a good advice to anyone proposing a
problem to have published their results long enough beforehand,
so a solution can be developed.

After the one month period, voting opens and for 2 weeks voters
can cast their votes.

In conclusion:

0. Proposing the vote   : as much time as it needs
1. Collecting options   : 4 weeks
2. Voting               : 2 weeks
"""

@app.route("/voting/propose", methods=["GET", "POST"])
def propose_vote():
    try:
        if request.method == "GET":
            response        = render_template("propose_vote.html")
        else:
            if not session.get("username"):
                raise Errors("not_logged_in")
            else:
                title           =   request.values["title"]
                description     =   request.values["description"]
                vote            =   { "title"           : title
                                    , "description"     : description
                                    , "stage"           : 0
                                    , "author"          :
                                    }
                vote["id"]      =   SHA256.new(json.dumps(vote).encode("utf-8")).hexdigest()
                elections.insert_one(vote)
                response    = redirect(f"/voting/option/{vote["id"]}")

    except Error as e:
        return e.status()
    except KeyError:
        return errors["invalid_data"]
    except Exception as e:
        raise e
    else:
        return response
###################################################################
############################ CRITICAL #############################
###################################################################

@app.route("/vote", methods=["POST", "GET"])
def vote():
    try:
        if request.method == "GET":
            election    = request.values['hash']
            election    = elections.find_one({ "hash" : election })
            election    = { key : election[key] for key in election if (key == "title" or key == "options") }
            response    = render_template("vote.html", election=election)
        else:
            app.logger.setLevel(100)

            if not session.get("username"):
                raise Error("invalid_context")
            username = session["username"]
            hash     = request.values['hash']
            vote     = json.loads(request.values['vote'])

            # Don't make or use encryption for voting **yet**
            election = elections.find_one({ "hash" : hash })
            if election:
                if username not in election["participants"]:
                    elections.update({ "$push" :    { "participants"    : username
                                                    , "votes"           : vote
                                                    }
                                })
                else:
                    raise Error("already_voted")
            else:
                raise Error("invalid_context")

            app.logger.setLevel(0)
            response = errors["OK"]
    except Error as e:
        return e.status()
    except (KeyError, TypeError):
        return errors["invalid_data"]
    except Exception as e:
        raise e
    else:
        return response

###################################################################
############################ /CRITICAL ############################
###################################################################

@app.route("/message", methods=["POST"])
def message():
    try:
        if not session.get("username") or not session.get("keys"):
            raise Error("invalid_context")

        author      = session["username"]
        body        = json.loads(request.values["body"])
        keys        = session["keys"]

        message     =   { "body"    : body
                        , "from"    : author
                        }

        Users.publish( message, keys )

    except KeyError:
        return errors["invalid_data"]
    except Error as e:
        return e.status()
    except Exception as e:
        raise e
    else:
        return errors["OK"]

# REGISTRATION

@app.route("/register", methods=["GET","POST"])
def register_route():
    try:
        if request.method == "GET":
            response    = render_template("register.html")
        else:
            if session["username"] != "joris":
                raise Error("invalid_context")
            else:
                username    = request.values["username"]
                id          = request.values["id"]
                passwords   = json.loads(request.values["passwords"])
                first_name  = request.values["first_name"]
                last_name   = request.values["last_name"]
                response    = register(username, id, passwords, first_name, last_name)
                response    = errors["OK"] if response else  errors["error_for_unknown_reason"]
    except Error as e:
        return e.status()
    except Exception as e:
        raise e
    else:
        return response

def register( username      : str
            , id_token      : str
            , passwords     : List[str]
            , first_name    : str
            , last_name     : str
            ):
    try:
        id              = SHA256.new(id_token.encode("utf-8")).hexdigest().encode("utf-8")
        passwords       = [SHA256.new(password.encode("utf-8")).hexdigest() for password in passwords]
        user            =   { "username"        : username
                            , "id"              : id
                            , "passwords"       : passwords
                            , "first_name"      : first_name
                            , "last_name"       : last_name
                            , "readings"        : []
                            , "writings"        : []
                            , "expiration"      : (datetime.timedelta (weeks=104
                                                                ,days=0
                                                                ,hours=0
                                                                ,minutes=0
                                                                ,seconds=0
                                                                ,milliseconds=0
                                                                ,microseconds=0
                                                                ) + datetime.datetime.now()).isoformat()
                            }

        if users.find_one({ "id" : id }) or users.find_one({ "username" : username }):
            raise Error("already_registered")
        else:
            users.insert_one(user)
    except Exception as e:
        raise e
    else:
        return True




# CRYPTOGRAPHY
from Crypto.Cipher      import AES, PKCS1_OAEP
from Crypto.Random      import get_random_bytes
from Crypto.Signature   import pkcs1_15

"""Encrypt string with AES Key and encrypt them with recipients public key.
Returns : (Signed encryption key, AES Nonce, tag, ciphertext)
"""
def encrypt(message : str, recipient_keys : RSA.RsaKey):
    try:
        # Create and encrypt AES Key
        aes_session_key = get_random_bytes(16)
        cipher_rsa      = PKCS1_OAEP.new(recipient_keys)
        enc_session_key = cipher_rsa.encrypt(aes_session_key)

        # Encrypt using previously generated AES Key.
        cipher_aes      = AES.new(aes_session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode("utf-8"))
    except Exception as e:
        raise e
    else:
        return (enc_session_key, cipher_aes.nonce, tag, ciphertext)


"""Inverse of encrypt and takes the results of encrypt and the private key of the recipient.
"""
def decrypt (recipients_private_key : RSA.RsaKey
            , enc_session_key : bytes
            , nonce : bytes
            , tag : bytes
            , ciphertext : bytes
            ):
    try:
        rsa_cipher      = PKCS1_OAEP.new(recipients_private_key)
        aes_session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes      = AES.new(aes_session_key, AES.MODE_EAX , nonce=nonce)
        message         = cipher_aes.decrypt_and_verify(ciphertext, tag)


    except ValueError:
        return False
    except Exception as e:
        raise e
    else:
        return message

"""Return signed hash of a string with private key.
Returns : (signature : bytes, hash : SHA256)
"""
def sign(message : str, author_key : RSA.RsaKey):
    hash        = SHA256.new(message.encode("utf-8")).hexdigest()
    signature   = pkcs1_15.new(author_key).sign(hash)
    return (signature, hash)

"""Verify a message signed by sign().
"""
def verify(signature : bytes, hash : SHA256, author_public_key : RSA.RsaKey):
    try:
        pkcs1_15.new(author_public_key).verify(hash, signature)
    except ValueError:
        return False
    except Exception as e:
        raise e
    else:
        return True
