"""
렌더링과 파서 기능을 담당하는 부분.
렌더링과 파서를 별도로 구분할 필요를 못 느껴서 하나로 관리.
"""
import os
import pathlib
from bs4 import BeautifulSoup
import re


def parse_article(contents: str) -> str:
    # parmalink_article : 게시글 보기 일 때에 해당하는 사항에 대한 변환.
    contents = contents.replace("<s_permalink_article_rep>", "{% if article_rep['type'] == 'permalink' %}")
    contents = contents.replace("</s_permalink_article_rep>", "{% endif %}")

    # protected article : 보호된 글에 대한 변환.
    contents = contents.replace("<s_article_protected>", "{% if article_protected %}")
    contents = contents.replace("</s_article_protected>", "{% endif %}")

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


def parse_index_article_rep(contents: str) -> str:
    """
    여기저기 가 있는 s_index_article_rep 를 모아서 s_list 뒷부분에 넣어준다.
    :param contents:
    :return:
    """
    s_article_protected = find_tags_inner_html('s_article_protected', contents)
    s_index_article_rep = find_tags_inner_html('s_index_article_rep', s_article_protected)
    # s_protected_index = re.findall(r'<s_index_article_rep>.*</s_index_article_rep>', s_protected, re.DOTALL)
    # s_protected_index = s_protected_index[0]

    index_article_protected = '{% if protected %}' + s_index_article_rep + '{% endif %}\n'
    # print(protected_index_article)

    s_article_rep = find_tags_inner_html('s_article_rep', contents)
    s_index_article_rep = find_tags_inner_html('s_index_article_rep', s_article_rep)
    index_article_normal = '{% if not protected %}' + s_index_article_rep + '{% endif %}\n'

    # s_list 바로 안쪽 끝에 붙이기. append 하기.
    # contents = re.sub(pattern='</', repl=r'', string=contents, flags=re.MULTILINE)
    contents = contents.replace("</s_list>", index_article_protected + index_article_normal + "</s_list>")
    return contents


def parse_notice(contents: str) -> str:
    contents = re.sub(pattern=r'<s_notice_rep_([^>]+)>', repl=r" {% if notice_rep[\g<1>] %}", string=contents,
                      flags=re.MULTILINE)
    contents = re.sub(pattern=r'</s_notice_rep_([^>]+)>', repl=r' {% endif %}', string=contents, flags=re.MULTILINE)
    return contents


def find_tags_inner_html(tag, context):
    """
    문자열에서 특정 태그로 감싸진 영역의 내부에 해당하는 html 텍스트를 반환하는 기능.
    단순한 태그에 해당해서만 가능함. 태그안에 attribute가 있다면... 그건 beautifulSoup을 이용하자...
    :param tag: 태그 명칭
    :param context: 입력값
    :return: html 텍스트
    """
    # r'<s_article_protected>.*</s_article_protected>' : outer_html
    # r'<s_article_protected>(.*)</s_article_protected>' : inner_html
    # regex = r'<' + re.escape(tag) + r'>(.*)</' + re.escape(tag) + r'>'  # 크게 찾을 때
    regex = r'<' + re.escape(tag) + r'>(.+?)</' + re.escape(tag) + r'>'
    ss = re.findall(regex, context, re.DOTALL)
    if len(ss) > 0:
        return ss[0]
    else:
        return ''


def remove_tag(tag, context):
    # r'<s_article_protected>.*</s_article_protected>' : outer_html
    # r'<s_article_protected>(.*)</s_article_protected>' : inner_html
    # 중복에 대한 처리가 안 되어 있네... 음... 어? * 을 +? 으로 바꾸니까 되네?
    # regex = r'<' + re.escape(tag) + r'>(.*)</' + re.escape(tag) + r'>'
    regex = r'<' + re.escape(tag) + r'>(.+?)</' + re.escape(tag) + r'>'
    context = re.sub(pattern=regex, repl='', string=context, flags=re.DOTALL)
    return context
