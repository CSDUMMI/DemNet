"""
Use Cryptodome.PublicKey.RSA
to generate random key pairs and store them in
MongoDB for the user.
This Key Pair is used for authenticating
messages and requests by the user.
This Module makes it possible to:
- Fetch the private key providing a password and username, login()
- Verify the signature of a user, is_author_of()
"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from pymongo import MongoClient
import datetime, sys

def users_collection():
    client = MongoClient()
    db = client.demnet
    return db.users

def login(username, password):
    users = users_collection()
    user = users.find_one({ 'username' : username })

    try:
        keys = RSA.import_key(user["private_key"], passphrase=password)

        if keys.publickey().export_key(format="PEM") != user["public_key"]:
            users.update_one({ "username" : username }, { "$set" : { "public_key"  : keys.publickey().export_key(format="PEM") } } )

        if datetime.datetime.strptime(user["expiration"], "%m/%d/%Y") > datetime.datetime.now():
"""
Use Cryptodome.PublicKey.RSA
to generate random key pairs and store them in
MongoDB for the user.
This Key Pair is used for authenticating
messages and requests by the user.
This Module makes it possible to:
- Fetch the private key providing a password and username, login()
- Verify the signature of a user, is_author_of()
"""
from Crypto.PublicKey import RSA
from pymongo import MongoClient
import datetime, sys

def users_collection():
    client = MongoClient()
    db = client.demnet
    return db.users

def login(username, password):
    users = users_collection()
    user = users.find_one({ 'username' : username })

    if not user:
        return False

    try:
        keys = RSA.import_key(user["private_key"], passphrase=password)

        if keys.publickey().export_key(format="PEM") != user["public_key"]:
            users.update_one({ "username" : username }, { "$set" : { "public_key"  : keys.publickey().export_key(format="PEM") } } )

        if datetime.datetime.strptime(user["expiration"], "%m/%d/%Y") > datetime.datetime.now():

            new_keys = RSA.generate(2048)
            new_expiration = datetime.timedelta (weeks=104
                                                ,days=0
                                                ,hours=0
                                                ,minutes=0
                                                ,seconds=0
                                                ,milliseconds=0
                                                ,microseconds=0
                                                ) + datetime.datetime.now()

            private_key = new_keys.export_key(format="PEM", passphrase=password)
            public_key  = new_keys.publickey().export_key(format="PEM")


            users.update_one(   { "username" : username }
                                , { "$set" : { "public_key"     : public_key
                                             , "private_key"    : private_key
                                             , "expiration"     : new_expiration
                                             }
                                  , "$push" : { "old_keys" :    { "expiration"  : user['expiration']
                                                                , "public_key"  : keys.publickey().export_key(format="PEM")
                                                                , "private_key" : user['private_key']
                                                                }
                                              }
                                  }
                                }
                            )

            keys = new_keys

        return keys

    except Exception as e:
        print("Invalid Login information", file=sys.stderr)
        return False
            new_keys = RSA.generate(2048)
            new_expiration = datetime.timedelta (weeks=104
                                                ,days=0
                                                ,hours=0
                                                ,minutes=0
                                                ,seconds=0
                                                ,milliseconds=0
                                                ,microseconds=0
                                                ) + datetime.datetime.now()

            private_key = new_keys.export_key(format="PEM", passphrase=password)
            public_key  = new_keys.publickey().export_key(format="PEM")


            users.update_one(   { "username" : username }
                                , { "$set" : { "public_key"     : public_key
                                             , "private_key"    : private_key
                                             , "expiration"     : new_expiration
                                             }
                                  , "$push" : { "old_keys" :    { "expiration"  : user['expiration']
                                                                , "public_key"  : keys.publickey().export_key(format="PEM")
                                                                , "private_key" : user['private_key']
                                                                }
                                              }
                                  }
                                }
                            )

            keys = new_keys

        return keys

    except Exception as e:
        print("Invalid Login information", file=sys.stderr)
        return False

"""
Verify that a string
was signed with the private key of
the user.
body : bytes
username : string
"""
def is_author_of(body,username,starts_with="FROM: "):
    users = users_collection()
    user = users.find_one({ "username" : username })

    if user:
        key = RSA.import_key(user['public_key'])
        cipher = PKCS1_OAEP.new(key)
        plain_text = cipher.decrypt(body)
        return (plain_text.startswith(starts_with), plain_text)
    else:
        return False
