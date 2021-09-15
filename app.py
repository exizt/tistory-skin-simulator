# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request, send_from_directory, render_template
import SkinLoader

app = Flask(__name__, static_url_path='/static')  # Flask 객체 선언.


@app.route("/", methods=["GET"])
def index():
    skins = SkinLoader.get_skins()

    html = ''
    for skin in skins:
        html += f'<a href="/{skin}">{skin}</a>'
    return html


@app.route("/<name>")
def render_skin(name):
    # return name
    return render_template('index.html')


# flask run -p 5000
# python -m flask run -p 5000
if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0', port=5000, debug=True)
