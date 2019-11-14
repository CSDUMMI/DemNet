#  ./data.py:
# - Store data as JSON Format
# - Save it to disk if necessary (try.. expect)
# - wait or reqests on local server ( flask )

try:
    from flask import Flask, request, jsonify
    app = Flask(__name__)
    save_file = open("demnet.data", "w+")

    # Data Model.
    # Everything is a JSON Object.
except Exception as e:
    raise
else:
    pass
