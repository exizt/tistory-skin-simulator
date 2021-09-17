import os
import pathlib
from bs4 import BeautifulSoup
import re

import SkinLoader
import SkinParser
import hashlib
# from xml.etree.ElementTree import parse as xml_parse
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element as XMLElement

XML_SKIN_ELEMENTS = {}


def get_skin_vars(skin_name):
    root = load(skin_name)
    xml_variables = root.find('variables')

    if xml_variables is None:
        return {}

    rv = {}
    for ss in xml_variables:
        if ss.tag == 'variablegroup':
            xml_var = ss.find('variable')
        else:
            xml_var = ss
        name = xml_var.find('name')
        default = xml_var.find('default')
        # print(name.text, default.text)
        if default is not None and default.text is not None \
                and len(str(default.text)) > 0:
            rv[name.text] = str(default.text)
    return rv


def load(skin_name) -> XMLElement:
    """
    xml 을 로드해서 파싱하는 기능.
    스킨명을 기준으로 경로를 찾고, 로드하고 모듈 변수에 대입하고 값을 반환한다.
    :param skin_name: 스킨이름
    :return: xml오브젝트
    """
    # xml 의 절대 경로
    skin_path = SkinLoader.get_skin_path(skin_name)
    xml_path = os.path.join(skin_path, 'index.xml')

    # xml 이 존재하지 않을 경우
    if not os.path.exists(xml_path):
        if skin_name in XML_SKIN_ELEMENTS:
            # xml_path가 없어진 skin_name에 한해서 목록에서 삭제
            del XML_SKIN_ELEMENTS[skin_name]
        # return False
        print('index.xml이 존재하지 않습니다. 생성해주세요.')
        raise

    if skin_name not in XML_SKIN_ELEMENTS:
        # XML_ROOT_ELEMENTS 에 없을 경우 XML을 로드
        XML_SKIN_ELEMENTS[skin_name] = load_by_path(xml_path)
    else:
        # 데이터가 오래된 경우를 비교해서 재생성
        pass

    return XML_SKIN_ELEMENTS[skin_name]


def load_by_path(xml_path: str) -> XMLElement:
    """
    xml을 로드하는 기능만 담당하는 기능.
    :param xml_path:xml의 절대경로
    :return:XMLElement
    """
    print('[SkinXML] Skin XML Load by path')
    # 예전 방식으로 file의 내용을 읽는 방식
    # with open(xml_path, 'r', encoding='utf-8') as f:
    #     context = f.read()

    # xml.etree.ElementTree 를 이용한 방식. (내장된 패키지임)
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # rv = root.find('skin')
    return root


def get_xml_path(skin_name=None) -> str:
    # index.xml 의 절대 경로를 생성
    skin_path = SkinLoader.get_skin_path(skin_name)
    xml_path = os.path.join(skin_path, 'index.xml')
    if os.path.exists(xml_path):
        return xml_path
    else:
        return ''
