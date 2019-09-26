#! /bin/usr/python3.5
from flask import Flask, request, render_template, send_from_directory, redirect, session, json
from Crypto.Hash import SHA256
import ipfshttpclient as ipfs

app            = Flask( __name__, static_folder = 'static', static_url_path = '' )
app.secret_key = Random.new( os.environ [ "SEED" ] ).read(16)

def connect():
    # Connect to the IPFS daemon running on the server on localhost!
    return ipfs.connect( '/ip4/127.0.0.1/tcp/5001/http' )
