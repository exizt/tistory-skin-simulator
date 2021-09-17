# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request, send_from_directory, render_template, Response
import SkinLoader
import SkinController as controller


app = Flask(__name__, static_url_path='/static')  # Flask 객체 선언.


@app.route("/", methods=["GET"])
def index():
    skins = SkinLoader.get_skins()

    html = '<ul>'
    for skin in skins:
        html += f'<li><a href="/{skin}/" target="_blank">{skin}</a></li>'
    html += "</ul>"
    return html


@app.route("/<skin_name>/")
def show_home(skin_name):
    # 유효한 스킨 이름인지 체크
    if not valid_skin(skin_name):
        return ''

    context = controller.wrap(skin_name, 'show_home')
    return render_template(SkinLoader.get_template_relpath(skin_name), **context)


@app.route("/<skin_name>/category")
def show_category(skin_name):
    # 유효한 스킨 이름인지 체크
    if not valid_skin(skin_name):
        return ''

    context = controller.wrap(skin_name, 'show_category')
    return render_template(SkinLoader.get_template_relpath(skin_name), **context)


@app.route("/<skin_name>/article")
def show_article(skin_name):
    # 유효한 스킨 이름인지 체크
    if not valid_skin(skin_name):
        return ''

    context = controller.wrap(skin_name, 'show_article')
    return render_template(SkinLoader.get_template_relpath(skin_name), **context)


@app.route("/<skin_name>/tags")
def show_tags(skin_name):
    # 유효한 스킨 이름인지 체크
    if not valid_skin(skin_name):
        return ''

    context = controller.wrap(skin_name, 'show_tags')
    return render_template(SkinLoader.get_template_relpath(skin_name), **context)


@app.route("/<skin_name>/guestbook")
def show_guestbook(skin_name):
    # 유효한 스킨 이름인지 체크
    if not valid_skin(skin_name):
        return ''

    context = controller.wrap(skin_name, 'show_guestbook')
    return render_template(SkinLoader.get_template_relpath(skin_name), **context)


def valid_skin(skin_name) -> bool:
    """
    유효한 스킨 이름인지 체크
    :param skin_name: 티스토리 스킨명
    :return:bool
    """
    skins = SkinLoader.get_skins()
    valid = skin_name in skins
    return valid


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
