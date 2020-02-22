# Introduction to running, testing and developing on DemNet
First: what is DemNet, currently?
It is a Flask Server and Client
in mostly HTML and CSS though a little JS
is used to dynamically request some data.

## Executing and Building
The Server is set up almost completely by the `start` script.
But somethings it can't handle on it's own yet:
### Requirements
1. Linux, this was only tested on Debian 10 Buster.
2. MongoDB and `mongod` running, as this is the Database we use
3. Python 3.7 or higher installed, as the Server is a Python Flask Server

## Starting
After you have installed these, the starting of the Server is easy.
The `start` script will install all dependencies from requirements.txt
build any files that need building and start the server.
If you don't want `start` to install the dependencies on your local installation
of Python, you should activate a virtualenv before executing:
```
$ SECRET_KEY=<some random string of characters (not really used for encryption)> ./start
```
After this the Server is listening on `http://127.0.0.1:8000`

## The Directory structure.
There are Three important folders in the repository
and 2-3 important files in the root directory.
### The `main.py` file.
