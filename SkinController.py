import os
import pathlib
import json
import re


def home(skin_name):
    """
    메인 페이지 (홈 화면)에 대한 핸들링.
    :return:
    """
    # 필요한 변수들을 셋팅하자...
    context = get_common_context(skin_name)

    cover_group = [
        {
            'name': 'cover-thumbnail-1',
            'title': '커버 타이틀 1',
            'data': [
                {
                    'url': '#',
                    'article_info': '...',
                    'title': '게시글',
                    'simple_date': '2021.09.14'
                },
                {
                    'url': '#',
                    'article_info': '...',
                    'title': '게시글',
                    'simple_date': '2021.09.14'
                },
                {
                    'url': '#',
                    'article_info': '...',
                    'title': '게시글',
                    'simple_date': '2021.09.14'
                }
            ]
        },
        {
            'name': 'cover-thumbnail-2',
            'title': '커버 타이틀 2',
            'data': [
                {
                    'url': '#',
                    'article_info': '...',
                    'title': '게시글',
                    'simple_date': '2021.09.14'
                },
                {
                    'url': '#',
                    'article_info': '...',
                    'title': '게시글',
                    'simple_date': '2021.09.14'
                },
                {
                    'url': '#',
                    'article_info': '...',
                    'title': '게시글',
                    'simple_date': '2021.09.14'
                },
                {
                    'url': '#',
                    'article_info': '...',
                    'title': '게시글',
                    'simple_date': '2021.09.14'
                }
            ]
        },
    ]
    context['cover_group'] = cover_group
    return context


def get_common_context(skin_name):
    """
    스킨 공통적인 설정에 대한 핸들링.
    :return:
    """
    context = get_blog_config_json()
    context['blog_menu'] = render_blog_menu(context['blog_menu'], skin_name)
    context['vars'] = {}

    # 사이드바에 대한 설정

    # 스킨 특유의 값에 대한 설정

    # 모든 스킨에 공통적인 부분에 대한 설정
    return context


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
