"""
렌더링과 파서 기능을 담당하는 부분.
렌더링과 파서를 별도로 구분할 필요를 못 느껴서 하나로 관리.
"""
import os
import pathlib
from bs4 import BeautifulSoup
import re


def parse_article(contents: str) -> str:
    contents = contents.replace("<s_permalink_article_rep>", "{% if article_rep['type'] == 'permalink' %}")
    contents = contents.replace("</s_permalink_article_rep>", "{% endif %}")
    
    # s_article_rep_ : article의 하위 값들. 작성일, 작성자, 링크, 제목 등
    contents = re.sub(pattern=r'<s_article_rep_([^>]+)>', repl=r" {% if article_rep[\g<1>] %}", string=contents,
                      flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_article_rep_([^>]+)>', repl=r' {% endif %}', string=contents, flags=re.MULTILINE)
    return contents


def parse_cover(contents: str) -> str:
    """
    s_cover 에 해당하는 부분을 렌더링
    :param contents: 문자열
    :return: str: 문자열
    """
    # s_cover_group 에 해당하는 부분을 변환
    contents = contents.replace("<s_cover_group>", "{% if cover_group %}")
    contents = contents.replace("</s_cover_group>", "{% endif %}")
    
    # s_cover 에 해당하는 부분을 변환
    contents = re.sub(pattern=r'<s_cover name=([^>]+)>', repl=r"{% if cover['type'] == \g<1> %}", string=contents,
                      flags=re.MULTILINE)
    contents = contents.replace("</s_cover>", "{% endif %}")
    
    # s_cover_item 에 해당하는 부분을 변환
    contents = contents.replace("<s_cover_item>", "{% for cover_item in cover['item'] %}")
    contents = contents.replace("</s_cover_item>", "{% endfor %}")

    # cover item 의 하위 요소에 대한 체크 루틴에 대한 변환
    contents = re.sub(pattern=r'<s_cover_item_([^>]+)>', repl=r"{% if cover_item[\g<1>] %}", string=contents,
                      flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_cover_item_([^>]+)>', repl=r' {% endif %}', string=contents, flags=re.MULTILINE)

    # cover_item 을 출력하는 부분을 변환
    contents = re.sub(pattern=r'\[##_cover_item_([^\]]+)_##\]', repl=r"{{ cover_item['\g<1>'] }}", string=contents,
                      flags=re.MULTILINE)

    # s_cover_rep에 대한 변환
    contents = contents.replace("<s_cover_rep>", "{% for cover in cover_group %}")
    contents = contents.replace("</s_cover_rep>", "{% endfor %}")

    # cover_title, cover_url 같은 것들에 대한 변환. (순서에 주의. 이 구문이 위로 가면 순서가 꼬일 수 있겠음)
    contents = re.sub(pattern=r'\[##_cover_([^\]]+)_##\]', repl=r'{{ cover[\g<1>] }}', string=contents,
                      flags=re.MULTILINE)
    # cover 요소에 대한 if 변환
    contents = re.sub(pattern=r'<s_cover_([^>]+)>', repl=r"{% if cover[\g<1>] %}", string=contents,
                      flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_cover_([^>]+)>', repl=r'{% endif %}', string=contents, flags=re.MULTILINE)
    return contents


def parse_notice(contents: str) -> str:
    contents = re.sub(pattern=r'<s_notice_rep_([^>]+)>', repl=r" {% if notice_rep[\g<1>] %}", string=contents,
                      flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_notice_rep_([^>]+)>', repl=r' {% endif %}', string=contents, flags=re.MULTILINE)
    return contents
