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
            "simple_date": "2021.09.16",
            "summary": "글 요약입니다",
            "desc": "글 본문입니다. 가나다라마바사아자차카타파하."
        },
        {
            "title": "게시글 제목",
            "link": "article",
            "simple_date": "2021.09.15",
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
    context['page_title'] = f"{skin_name} 스킨"
    context['blog_menu'] = render_blog_menu(context['blog_menu'], skin_name)
    context['vars'] = SkinXML.get_skin_vars(skin_name)
    context['tags'] = get_tags()

    # 사이드바에 대한 설정

    # 스킨 특유의 값에 대한 설정

    # 모든 스킨에 공통적인 부분에 대한 설정
    return context


def render_skin(skin_name):
    """
    스킨의 정보를 조회하고 템플릿파일로 렌더링한다.
    변경 상태 등을 체크하면서 렌더링을 해준다.
    :param skin_name:
    :return:
    """
    # 스킨 목록을 조회
    skins = SkinLoader.get_skins()
    valid = skin_name in skins
    if not valid:
        # skins 폴더에 없는 스킨명이므로 아무것도 안 함. 잘못된 접근임.
        return ''

    # 스킨 템플릿 캐시 폴더가 없는 상태라면 폴더 생성
    cache_dir = SkinLoader.get_templates_cache_dir_path()
    if not os.path.exists(cache_dir):
        print('create skin_cache directory.')
        os.makedirs(cache_dir)

    # 스킨 템플릿 캐시 파일이 존재하는지 여부
    if not os.path.exists(SkinLoader.get_template_file_path(skin_name)):
        # 스킨 템플릿 캐시 파일 재생성
        print(f'build skin template cache..({skin_name})')
        render_skin_to_template(skin_name)

    # skin.html 파일과 스킨 템플릿 캐시 파일의 최종 변경시간을 비교
    sk_mtime = SkinLoader.get_skin_mtime(skin_name)
    tp_mtime = SkinLoader.get_template_file_mtime(skin_name)
    if sk_mtime > tp_mtime + 10:
        # 템플릿이 오래되었으므로 재생성
        print(f'rebuild skin template cache..({skin_name})')
        render_skin_to_template(skin_name)


def render_skin_to_template(skin_name):
    SkinLoader.to_template(skin_name)


def get_blog_config_json():
    return get_data_json('config.json')


def get_data_json(file_name):
    curpath = pathlib.Path(__file__).parent.absolute()
    path = os.path.join(curpath, 'data')
    path = os.path.join(path, file_name)
    with open(path, 'r', encoding='utf-8') as f:
        # context = f.read()
        context = json.load(f)
    return context


def get_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
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
