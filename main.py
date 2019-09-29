#! /bin/usr/python3.5
import json
import ipfshttpclient as ipfs

app             = Flask( __name__, static_folder = 'static', static_url_path = '' )
app.secret_key  = Random.new( os.environ [ "SEED" ] ).read(16)

users_index     = os.environ[ "USER_INDEX" ]

"""
Connect to IPFS Daemon
"""
def connect():
    # Connect to the IPFS daemon running on the server on localhost!
    return ipfs.connect( '/ip4/127.0.0.1/tcp/5001/http' )

"""
get_users_data:
Load List of JSON Objects from
IPFS
"""
def get_users_data():
    client = connect()
    users  = client.cat( users_index )
    users  = users.split( "\n" )

    for i in range( len( users ) ):
        users[i] = client.cat ( users[i] )
        users[i] = json.loads( users[i] )

    return users

"""
Initialize election,
thus making this server
the supervisor of the election.
"""
def init_election():
        get_users_data()
