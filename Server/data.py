#  ./data.py:
# - Store data as JSON Format
# - Save it to disk if necessary (try.. expect)
# - wait or reqests on local server ( flask )

try:
    from flask import Flask, request, jsonify
    app = Flask(__name__)
    save_file = open("demnet.data", "w+")
    root = json.load(save_file)
    # Data Model.
    # Everything is a JSON Object.
    # There is a single JSON Object root.
    # That's what is saved in save_file
    # Any  object is part of root
    # Any object is indexed using
    @app.route("/save/<string:object_name>")
    def save(object_name):
        root[object_name] = request.values["object"]
        return ("Changed " + object_name)

    @app.route("/fetch/<string:object_name>")
    def fetch(object_name):
        return jsonify(root[object_name])

    @app.route("/error")
    def error():
        x = 1/0
        return x
    app.run(port=8008)
except Exception as e:
    raise
else:
    pass
