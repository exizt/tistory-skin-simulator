import os
import pathlib
import json
import re
import SkinXML
import SkinLoader


def wrap(skin_name, route):
    # 스킨의 flask 템플릿 생성 혹은 재로드
    render_skin(skin_name)

    # 사용할 변수들
    context = get_common_context(skin_name)

    if route == 'show_home':
        context = show_home(skin_name, context)
    elif route == 'show_category':
        context = show_category(skin_name, context)
    elif route == 'show_article':
        context = show_article(skin_name, context)
    elif route == 'show_tags':
        context = show_tags(skin_name, context)
    elif route == 'show_guestbook':
        context = show_guestbook(skin_name, context)

    return context


def show_home(skin_name, context):
    """
    메인 페이지 (홈 화면)에 대한 핸들링.
    :return:
    """
    # 초기값
    cover_group = None
    
    # 스킨의 index.xml 을 읽어오는 부분.
    xml = SkinXML.load(skin_name)
    # xml_cover = xml.find('default').find('cover')
    xml_default = xml.find('default')

    if xml_default is not None:
        xml_cover = xml_default.find('cover')
        if xml_cover is not None:
            cover_text = xml_cover.text
            # print(cover_text)
            cover_group = json.loads(cover_text)

        # print(xml_cover)

    if cover_group is None:
        # 글 목록을 조회하는 방식으로

        # context 에 추가 (퍼머링크 방식)
        context['article_list_info'] = get_article_list_info()
        context['article_index_list'] = get_article_index_list()
        
        # s_list 방식
        context['article_list_legacy'] = get_article_index_list()
    else:
        context['cover_group'] = cover_group

    # context
    context['body_id'] = 'tt-body-index'
    return context


# noinspection PyUnusedLocal
def show_category(skin_name, context):
    """
    카테고리. (글 목록)
    :return:
    """
    # 게시글 목록
    article_list = get_article_index_list()
    article_list_info = get_article_list_info()

    # s_list 방식
    context['article_list_legacy'] = get_article_index_list()

    # context 에 추가
    context['article_list_info'] = article_list_info
    context['article_index_list'] = article_list
    context['body_id'] = 'tt-body-category'

    return context


# noinspection PyUnusedLocal
def show_article(skin_name, context):
    """
    게시글 (하나의 글)
    :return:
    """
    article_index_list = get_article_index_list()
    # 하나만 선택.
    article_index_list = [article_index_list[0]]
    # print(type([article_index_list]))

    # context 에 추가
    context['article_index_list'] = article_index_list
    context['body_id'] = 'tt-body-page'

    return context


# noinspection PyUnusedLocal
def show_tags(skin_name, context):
    """
    태그 목록
    :return:
    """
    # context 에 추가
    # context['tags'] = get_tags()
    context['body_id'] = 'tt-body-tag'
    context['route_type'] = 'tags'
    return context


# noinspection PyUnusedLocal
def show_guestbook(skin_name, context):
    """
    방명록
    :return:
    """
    # context 에 추가
    context['guest'] = True
    context['guest_list'] = get_guestbook_list()
    context['body_id'] = 'tt-body-guestbook'

    return context


def get_article_list_info():
    article_list_info = {
        'conform': '프로그래밍/IT',
        'count': '59',
        'description': '목록/카테고리에 대한 설명글'
    }
    return article_list_info


def get_article_index_list():
    article_list = [
        {
            "title": "게시글 제목",
            "link": "article",
            "simple_date": "2021.09.14",
            "summary": "글 요약입니다",
            "desc": "글 본문입니다"
        },
        {
            "title": "게시글 제목",
            "link": "article",
            "simple_date": "2021.09.14",
            "summary": "글 요약입니다",
            "desc": "글 본문입니다"
        },
        {
            "title": "게시글 제목",
            "link": "article",
            "simple_date": "2021.09.14",
            "summary": "글 요약입니다",
            "desc": "글 본문입니다"
        }
    ]
    return article_list


def get_guestbook_list():
    data = [
        {
            "name": "홍길동",
            "date": "2021.09.17",
            "desc": "안녕하세요"
        },
        {
            "name": "홍길동",
            "date": "2021.09.17",
            "desc": "반가워요",
            "reply": [
                {
                    "name": "고길동",
                    "date": "2021.09.17",
                    "desc": "처음 뵙겠습니다"
                }
            ]
        },
        {
            "name": "홍길동",
            "date": "2021.09.17",
            "desc": "처음 뵙겠습니다",
            "reply": [
                {
                    "name": "홍길동",
                    "date": "2021.09.17",
                    "desc": "질문이 있어요"
                }
            ]
        }
    ]
    return data


def get_tags():
    tags = [
        {
            "link": "#",
            "name": "Windows"
        },
        {
            "link": "#",
            "name": "티스토리"
        },
        {
            "link": "#",
            "name": "경제"
        },
        {
            "link": "#",
            "name": "IT"
        },
        {
            "link": "#",
            "name": "기획"
        }
    ]
    return tags


def get_common_context(skin_name):
    """
    스킨 공통적인 설정에 대한 핸들링.
    :return:
    """
    context = get_blog_config_json()
    context['blog_menu'] = render_blog_menu(context['blog_menu'], skin_name)
    context['vars'] = SkinXML.get_skin_vars(skin_name)
    context['tags'] = get_tags()

    # 사이드바에 대한 설정

    # 스킨 특유의 값에 대한 설정

    # 모든 스킨에 공통적인 부분에 대한 설정
    return context


def render_skin(skin_name):
    skins = SkinLoader.get_skins()
    valid = skin_name in skins
    if not valid:
        return ''

    if not os.path.exists(SkinLoader.get_template_path(skin_name)):
        # 템플릿이 없으므로 재생성
        SkinLoader.render_skin(skin_name)

    # 파일의 변경 시간을 조회
    sk_mtime = SkinLoader.get_skin_mtime(skin_name)
    tp_mtime = SkinLoader.get_template_mtime(skin_name)

    if sk_mtime > tp_mtime + 100:
        # 템플릿이 오래되었으므로 재생성
        print('rebuild skin templates')
        SkinLoader.render_skin(skin_name)


def get_blog_config_json():
    return get_json('config.json')


def get_json(file_name):
    curpath = pathlib.Path(__file__).parent.absolute()
    path = os.path.join(curpath, 'data')
    path = os.path.join(path, file_name)
    with open(path, 'r', encoding='utf-8') as f:
        # context = f.read()
        context = json.load(f)
    return context


def render_blog_menu(blog_menu, skin_name):
    # context = context.replace('<a href=\"/\"', f'<a href=\"/{skin_name}/\"')
    # context = context.replace('<a href=\"/tag\"', f'<a href=\"/{skin_name}/tag\"')
    # context = context.replace('<a href=\"/media\"', f'<a href=\"/{skin_name}/media\"')
    # context = context.replace('<a href=\"/location\"', f'<a href=\"/{skin_name}/location\"')
    # context = context.replace('<a href=\"/guestbook\"', f'<a href=\"/{skin_name}/guestbook\"')
    blog_menu = re.sub(pattern=r'<a href="/([^"]*)"', repl=r'<a href="/' + skin_name + r'/\g<1>"',
                       string=blog_menu,
                       flags=re.MULTILINE)

    return blog_menu
