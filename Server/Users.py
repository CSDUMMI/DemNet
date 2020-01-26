"""
Use Cryptodome.PublicKey.RSA
to generate random key pairs and store them in
MongoDB for the user.
This Key Pair is used for authenticating
messages and requests by the user.
This Module makes it possible to:
- Fetch the private key providing a passphrase and username, login()
- Verify the signature of a user, is_author_of()
"""
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from pymongo import MongoClient
import datetime, sys, json

client = MongoClient()
db = client.demnet
users = db.users


def login(username, passphrase):
    user = users.find_one({ 'username' : username })

    if not user:
        return False

    try:
        keys = RSA.import_key(user["private_key"], passphrase=passphrase)

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

            private_key = new_keys.export_key(format="PEM", passphrase=passphrase)
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
    user = users.find_one({ "username" : username })

    if user:
        key = RSA.import_key(user['public_key'])
        cipher = PKCS1_OAEP.new(key)
        plain_text = cipher.decrypt(body)
        return (plain_text.startswith(starts_with), plain_text)
    else:
        return False


"""
Encrypt a message or post before it is being send.
message is a real message document.
Encryption of a message:
Ciphertext = E(E(message,private_key_author), public_key_recipient)
If recipient = "all" then the last encryption step is skipped.
Parameters:
- message (dict) a full message document as defined in Database.md
- keys, the RSA Keys of the author
Returns:
Either `False` or a list of dictionaries of the kind:
{ "recipient_name" : recipient_username, "ciphertext" : ciphertext }

"""
def encrypt(message,keys):
    user = users.find_one({ "username" : message["from"] })

    if user:
        try:
            if "all" in user['to']:
                # Skip encryption if only one of the recipients is "all".
                ciphertexts = [{ "all" : message['body'] }]
            else:
                plain_text = json.dumps(message['body']).encode('utf-8') # Make the body into a string
                cipher = PKCS1_OAEP.new(keys)
                ciphertext = cipher.encrypt(plain_text)
                ciphertexts = []
                for recipient_name in message['to']:
                    recipient = users.find_one({ "username" : recipient_name })
                    if recipient:
                        recipient_public_key = RSA.import_key(recipient['public_key'])
                        recipient_cipher = PKCS1_OAEP.new(recipient_public_key)

                        ciphertexts.append({ "recipient" : recipient_name, "ciphertext" : recipient_cipher.encrypt(ciphertext) })

            return ciphertexts
        except Exception as e:
            return False

"""
Publishing a message works in these steps:
1. Encrypt/Sign the message
2. Publish it in demnet.messages
3. Add a notification to the recipient's feed.
Parameters:
- *message* message document with unencrypted body
- *passphrase* passphrase to encrypt the author's private key
Returns:
True if successfull
False if not
"""
def publish(message, passphrase):
    # 1. Encrypt/Sign the message
    body = encrypt(message, passphrase)
    if body != False:
        # 2. Publish it in demnet.messages
        message['body'] = body
        message['hash'] = SHA256.new(json.dumps(body).encode('utf-8')).hexdigest()
        messages = db.messages
        messages.insert_one(message)

        # 3. Add a notification to the recipient's feed
        for recipient_name in message['to']:
            users.update_one({ "username" : recipient_name }
                             , { "$push" : { "feed" : message["hash"] } }
                            )
        return True
    return False
