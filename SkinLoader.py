import os
import pathlib
from bs4 import BeautifulSoup
import re


def get_skins() -> list:
    """
    스킨 목록을 조회
    :return:list:스킨 목록
    """
    # skins 디렉토리의 경로
    skins_path = get_skins_dir_path()
    # skin의 목록
    skins = os.listdir(skins_path)
    if len(skins) > 0:
        return skins
    else:
        return []


def get_current_path():
    """
    현재 파일의 경로를 가져오는 기능
    :return:obj:현재 파일의 절대 경로
    """
    # 현재 파일의 경로
    return pathlib.Path(__file__).parent.absolute()


def get_skins_dir_path() -> str:
    """
    skins 디렉토리의 경로를 가져오는 기능
    :return: skins 디렉토리의 절대 경로
    """
    # skins 디렉토리의 경로
    skins_path = os.path.join(get_current_path(), 'skins')
    return skins_path


def get_skin_raw(skin_name: str) -> str:
    """
    스킨의 내용을 가져오는 기능
    :param skin_name: 스킨 폴더의 이름
    :return: 스킨의 내용
    """
    skins_dir = get_skins_dir_path()
    skin_path = os.path.join(skins_dir, skin_name)
    html_path = os.path.join(skin_path, 'skin.html')

    with open(html_path, 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents


def render_skin(skin_name):
    contents = get_skin_raw(skin_name)

    # 게시글
    # contents = contents.replace("<s_article_rep>", "{% if mode 'article' %}")
    # contents = contents.replace("</s_article_rep>", "{% endif %}")

    # s_if_var_ 와 s_not_var 는 정규식으로 처리
    contents = re.sub(pattern=r'<s_if_var_([^>]+)>', repl=r'{% if \g<1> %}', string=contents, flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_if_var_([^>]+)>', repl='{% endif %}', string=contents, flags=re.MULTILINE)
    # s_not_var
    contents = re.sub(pattern=r'<s_not_var_([^>]+)>', repl=r'{% if not \g<1> %}', string=contents, flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_not_var_([^>]+)>', repl='{% endif %}', string=contents, flags=re.MULTILINE)

    changes = [
        ["<s_article_rep>", "{% if mode 'article' %}"],
        ["<s_search>", "{% if mode 'article' %}"],
        ["<s_cover_group>", "{% if mode 'article' %}"],
        ["<s_cover_rep>", "{% if mode 'article' %}"],
        ["<s_cover_item>", "{% if mode 'article' %}"],
        ["</s_cover_item>", "{% if mode 'article' %}"],
        ["<s_cover_url>", "{% if mode 'article' %}"],
        ["<s_cover_item_article_info>", "{% if mode 'article' %}"],
        ["<s_cover_item_thumbnail>", "{% if mode 'article' %}"],
        ["<s_page_rep>", "{% if mode 'article' %}"],
        ["<s_notice_rep>", "{% if mode 'article' %}"],
        ["<s_notice_rep_thumbnail>", "{% if mode 'article' %}"],
        ["<s_list>", "{% if mode 'article' %}"],
        ["<s_list_empty>", "{% if mode 'article' %}"],
        ["<s_article_protected>", "{% if mode 'article' %}"],
        ["<s_index_article_rep>", "{% if mode 'article' %}"],
        ["<s_permalink_article_rep>", "{% if mode 'article' %}"],
        ["<s_ad_div>", "{% if mode 'article' %}"],
        ["<s_tag_label>", "{% if mode 'article' %}"],
        ["<s_article_protected>", "{% if mode 'article' %}"],
        ["<s_article_protected>", "{% if mode 'article' %}"],

    ]
    # 아예 여러개 있으면 여러번 돌고 하나만 있으면 하나만 도는 식으로 처리하는 게 나으려나?
    # 보니까 _rep 는 repeat 인 거 같다?
    contents = re.sub(pattern=r'<s_([^>]+)_rep>', repl=r'{% for \g<1>_rep in \g<1>_list %}', string=contents, flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_([^>]+)_rep>', repl=r'{% endfor %}', string=contents, flags=re.MULTILINE)

    # 글 목록 (s_list)
    # 두 가지의 경우가 있는데, s_index_article_rep 를 이용하는 방식과 s_list_rep를 이용한 방식이 있다.
    contents = contents.replace("<s_list_rep>", "{% for list in list_list %}")
    contents = contents.replace("</s_list_rep>", "{% endfor %}")

    # contents = re.sub(pattern=r'<s_([^>]+)_rep>', repl=r'{% for i in \g<1> %}', string=contents, flags=re.MULTILINE)
    # s_cover 는 name 값을 갖고 있어서, 얘는 별도로.

    
    templates_path = os.path.join(get_current_path(), 'templates/test.html')
    with open(templates_path, 'w', encoding='utf-8') as f:
        f.write(contents)
    # soup = BeautifulSoup(contents, 'lxml')
    # print(soup.head)
    # ss = soup.find('s_index_article_rep')
    # print(ss)
