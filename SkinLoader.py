import os
import pathlib
from bs4 import BeautifulSoup
import re
import SkinParser


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

    # var 의 dash 방지 (스킨에 따라서 그런 경우가 있길래...)
    contents = re.sub(pattern=r'</?s_(if|not)_var_([^>]+)>', repl=lambda m: m.group().replace("-", "_"),
                      string=contents, flags=re.MULTILINE)
    contents = re.sub(pattern=r'\[##_var_([^\]]+)_##\]', repl=lambda m: m.group().replace("-", "_"),
                      string=contents, flags=re.MULTILINE)

    # s_if_var_ 와 s_not_var 는 정규식으로 처리
    contents = re.sub(pattern=r'<s_if_var_([^>]+)>', repl=r" {% if vars.\g<1> is not none %}", string=contents, flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_if_var_([^>]+)>', repl=' {% endif %}', string=contents, flags=re.MULTILINE)
    # s_not_var
    contents = re.sub(pattern=r'<s_not_var_([^>]+)>', repl=r" {% if vars.\g<1> is none or not vars['\g<1>'] %}", string=contents, flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_not_var_([^>]+)>', repl=' {% endif %}', string=contents, flags=re.MULTILINE)
    # var 출력되는 부분 처리
    contents = re.sub(pattern=r'\[##_var_([^\]]+)_##\]', repl=r"{{ vars.\g<1> }}", string=contents,
                      flags=re.MULTILINE)

    # index_article 에서 index_article_rep 로 처리된 게 있으면 s_list 후반부에 붙이기
    contents = SkinParser.parse_index_article_rep(contents)

    # 원래 있던 protected index_article_rep 는 제거하기.
    contents = SkinParser.remove_tag('s_index_article_rep', contents)
    
    # s_list 를 변환
    contents = contents.replace("<s_list>", "{% if list %}")
    contents = contents.replace("</s_list>", "{% endif %}")

    # cover 기능
    contents = SkinParser.parse_cover(contents)

    # notice 관련.
    contents = SkinParser.parse_notice(contents)

    # article 관련.
    contents = SkinParser.parse_article(contents)

    # 아예 여러개 있으면 여러번 돌고 하나만 있으면 하나만 도는 식으로 처리하는 게 나으려나?
    # 보니까 _rep 는 repeat 인 거 같다?
    contents = re.sub(pattern=r'<s_([^>]+)_rep>', repl=r'{% for \g<1>_rep in \g<1>_list %}', string=contents, flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_([^>]+)_rep>', repl=r'{% endfor %}', string=contents, flags=re.MULTILINE)

    # 글 목록 (s_list)
    # 두 가지의 경우가 있는데, s_index_article_rep 를 이용하는 방식과 s_list_rep를 이용한 방식이 있다.
    # contents = contents.replace("<s_list_rep>", "{% for list_rep in list_list %}")
    # contents = contents.replace("</s_list_rep>", "{% endfor %}")

    contents = re.sub(pattern=r'\[##_list_rep_([^\]]+)_##\]', repl=r'{{list_rep\[ \g<1> \]}}', string=contents,
                      flags=re.MULTILINE)

    # s_list 에서 처리. s_index_article_rep에 대한 내용을 넣어줄 필요가 있다. 이 경우 파싱을 해야할 듯?
    # s_list 뒤에 붙이면 되려나? for 블라블라 if protected else endif 같은 느낌?

    # contents = re.sub(pattern=r'<s_([^>]+)_rep>', repl=r'{% for i in \g<1> %}', string=contents, flags=re.MULTILINE)
    # s_cover 는 name 값을 갖고 있어서, 얘는 별도로.

    
    templates_path = os.path.join(get_current_path(), 'templates/test.html')
    with open(templates_path, 'w', encoding='utf-8') as f:
        f.write(contents)
    # soup = BeautifulSoup(contents, 'lxml')
    # print(soup.head)
    # ss = soup.find('s_index_article_rep')
    # print(ss)
