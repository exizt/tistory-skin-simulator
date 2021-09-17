import os
import pathlib
from bs4 import BeautifulSoup
import re

import SkinParser
import hashlib


def get_skins() -> list:
    """
    스킨 목록을 조회
    :return:list:스킨 목록
    """
    # skins 디렉토리의 경로
    skins_path = get_skins_dir_path()
    # skin의 목록
    # skins = os.listdir(skins_path)
    skins = [name for name in os.listdir(skins_path) if os.path.isdir(os.path.join(skins_path, name))]
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


def get_skin_path(skin_name: str) -> str:
    skins_dir = get_skins_dir_path()
    skin_path = os.path.join(skins_dir, skin_name)
    return skin_path


def get_skin_html_path(skin_name: str):
    skin_path = get_skin_path(skin_name)
    html_path = os.path.join(skin_path, 'skin.html')
    return html_path


def read_skin_raw(skin_name: str) -> str:
    """
    스킨의 내용을 가져오는 기능
    :param skin_name: 스킨 폴더의 이름
    :return: 스킨의 내용
    """
    with open(get_skin_html_path(skin_name), 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents


def get_skin_mtime(skin_name):
    return os.path.getmtime(get_skin_html_path(skin_name))


def get_template_filename(skin_name):
    return f'{skin_name}_skin.html'


def get_template_path(skin_name):
    templates_path = os.path.join(get_current_path(), 'templates')
    templates_path = os.path.join(templates_path, 'skin_cache')
    templates_path = os.path.join(templates_path, get_template_filename(skin_name))
    return templates_path


def get_template_relpath(skin_name):
    return 'skin_cache/'+get_template_filename(skin_name)


def get_template_mtime(skin_name):
    return os.path.getmtime(get_template_path(skin_name))


def render_skin(skin_name):
    context = read_skin_raw(skin_name)

    # 공통
    context = context.replace("[##_body_id_##]", "{{ body_id }}")
    context = context.replace("[##_page_title_##]", f"{skin_name} 스킨")

    # 전체를 감싸는 태그
    context = re.sub(pattern=r'</?s_t3>', repl="", string=context, flags=re.MULTILINE)
    # 광고 관련 태그
    context = context.replace("[##_revenue_list_upper_##]", "")
    context = context.replace("[##_revenue_list_lower_##]", "")
    # 이따금 오류 일으킬 소지가 있음.
    context = context.replace("[##_article_rep_thumbnail_raw_url_##]", "")
    # 불필요한 경우들 (작업하려면 봐야하므로)
    context = re.sub(pattern=r'</?s_search>', repl="", string=context, flags=re.MULTILINE)
    context = re.sub(pattern=r'</?s_ad_div>', repl="", string=context, flags=re.MULTILINE)

    # s_if_var_ 와 s_not_var 를 변환
    context = SkinParser.parse_skin_var(context)

    # cover 기능
    context = SkinParser.parse_cover(context)

    # notice 관련.
    context = SkinParser.parse_notice(context)

    # s_index_article_rep 관련.
    context = SkinParser.parse_index_article_rep(context)

    # s_list 와 관련된 것 변환.
    context = SkinParser.parse_s_list(context)

    # article 관련.
    context = SkinParser.parse_article(context)

    # guest 관련.
    context = SkinParser.parse_guest(context)

    # tag 관련
    context = SkinParser.parse_tag(context)

    # sidebar 관련
    context = SkinParser.parse_sidebar(context)

    # 위치 로그 관련
    context = SkinParser.parse_location_log(context)

    # 아예 여러개 있으면 여러번 돌고 하나만 있으면 하나만 도는 식으로 처리하는 게 나으려나?
    # 보니까 남은 것 중 _rep 는 repeat 인 거 같다?
    context = re.sub(pattern=r'<s_([^>]+)_rep>', repl=r'{% for \g<1>_rep in \g<1>_list %}', string=context, flags=re.MULTILINE)
    context = re.sub(pattern=r'</s_([^>]+)_rep>', repl=r'{% endfor %}', string=context, flags=re.MULTILINE)

    # 기타 변수들 (한 번에 바꿔도 되는데. 그건 어느 정도 정리 된 후에 하자. 지금은 조금 이른 듯.
    # 블로그 제목
    context = context.replace("[##_title_##]", "{{ title }}")
    # 프로필 이미지, 또는 블로그 대표 이미지
    context = context.replace("[##_image_##]", "{{ image }}")
    # 블로거 필명
    context = context.replace("[##_blogger_##]", "{{ blogger }}")
    # 블로그 설명
    context = context.replace("[##_desc_##]", "{{ desc }}")
    # 블로그 url
    context = context.replace("[##_blog_link_##]", "{{ blog_link }}")
    # rss_url
    context = context.replace("[##_rss_url_##]", "#")
    # 카운트들
    context = context.replace("[##_count_total_##]", "{{ count_total }}")
    context = context.replace("[##_count_today_##]", "{{ count_today }}")
    context = context.replace("[##_count_yesterday_##]", "{{ count_yesterday }}")
    context = context.replace("[##_search_name_##]", "")
    context = context.replace("[##_search_onclick_submit_##]", "")
    context = context.replace("[##_search_text_##]", "검색어")
    context = context.replace("[##_owner_url_##]", "#")
    context = context.replace("[##_blog_menu_##]", "{{ blog_menu|safe }}")
    context = context.replace("[##_guestbook_link_##]", "./guestbook")
    context = context.replace("[##_taglog_link_##]", "./tags")

    # contents = re.sub(pattern=r'<s_([^>]+)_rep>', repl=r'{% for i in \g<1> %}', string=contents, flags=re.MULTILINE)
    # s_cover 는 name 값을 갖고 있어서, 얘는 별도로.

    # 템플릿 파일로 생성
    with open(get_template_path(skin_name), 'w', encoding='utf-8') as f:
        f.write(context)
