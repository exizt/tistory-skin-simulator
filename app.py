# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_url_path='/static')  # Flask 객체 선언.


@app.route("/", methods=["GET"])
def index():
    return 'ddd'


# flask run -p 5000
if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0', port=5000, debug=True)
