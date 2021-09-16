import os
import pathlib
from bs4 import BeautifulSoup
import re
import SkinParser
import json


def home():
    """
    메인 페이지 (홈 화면)에 대한 핸들링.
    :return:
    """
    # 필요한 변수들을 셋팅하자...
    context = get_blog_config_json()
    context['vars'] = {}
    return context


def common():
    """
    스킨 공통적인 설정에 대한 핸들링.
    :return:
    """
    # noinspection PyDictCreation
    result = {}
    # 사이드바에 대한 설정

    # 스킨 특유의 값에 대한 설정

    # 모든 스킨에 공통적인 부분에 대한 설정


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
