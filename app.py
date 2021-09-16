# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request, send_from_directory, render_template, Response
import SkinLoader
import SkinController as controller


app = Flask(__name__, static_url_path='/static')  # Flask 객체 선언.


@app.route("/", methods=["GET"])
def index():
    skins = SkinLoader.get_skins()

    html = ''
    for skin in skins:
        html += f'<a href="/{skin}/">{skin}</a>'
    return 'html'


@app.route("/<skin_name>/")
def render_skin(skin_name):
    skins = SkinLoader.get_skins()
    valid = skin_name in skins
    if not valid:
        return ''

    # return name
    sk_mtime = SkinLoader.get_skin_mtime(skin_name)
    tp_mtime = SkinLoader.get_template_mtime(skin_name)

    if sk_mtime > tp_mtime + 100:
        # 재 생성 해야됨
        print('rebuild skin templates')
        SkinLoader.render_skin(skin_name)

    context = controller.home()
    return render_template(SkinLoader.get_template_name(skin_name), **context)


@app.route("/<name>/style.css")
def skin_style(name):
    return send_from_directory(f'skins/{name}', 'style.css')


@app.route("/<name>/images/<file_name>")
def skin_file(name, file_name):
    return send_from_directory(f'skins/{name}/images', file_name)


# flask run -p 5000
# python -m flask run -p 5000
if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0', port=5000, debug=True)
