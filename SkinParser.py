"""
렌더링과 파서 기능을 담당하는 부분.
렌더링과 파서를 별도로 구분할 필요를 못 느껴서 하나로 관리.
"""
import os
import pathlib
from bs4 import BeautifulSoup
import re


def parse_cover(context: str) -> str:
    """
    s_cover 에 해당하는 부분을 렌더링
    :param context: 문자열
    :return: str: 문자열
    """
    # s_cover_group 에 해당하는 부분을 변환
    context = context.replace("<s_cover_group>", "{% if cover_group %}")
    context = context.replace("</s_cover_group>", "{% endif %}")

    # s_cover 에 해당하는 부분을 변환
    context = re.sub(pattern=r'<s_cover name=([^>]+)>', repl=r"{% if cover['name'] == \g<1> %}", string=context,
                     flags=re.MULTILINE)
    context = context.replace("</s_cover>", "{% endif %}")

    # s_cover_item 에 해당하는 부분을 변환
    context = context.replace("<s_cover_item>", "{% for cover_item in cover['data'] %}")
    context = context.replace("</s_cover_item>", "{% endfor %}")

    # cover item 의 하위 요소에 대한 체크 루틴에 대한 변환
    context = re.sub(pattern=r'<s_cover_item_([^>]+)>', repl=r"{% if cover_item.\g<1> %}", string=context,
                     flags=re.MULTILINE)
    context = re.sub(pattern=r'</s_cover_item_([^>]+)>', repl=r' {% endif %}', string=context, flags=re.MULTILINE)

    # cover_item 을 출력하는 부분을 변환
    context = re.sub(pattern=r'\[##_cover_item_([^\]]+)_##\]', repl=r"{{ cover_item['\g<1>'] }}", string=context,
                     flags=re.MULTILINE)

    # s_cover_rep에 대한 변환
    context = context.replace("<s_cover_rep>", "{% for cover in cover_group %}")
    context = context.replace("</s_cover_rep>", "{% endfor %}")

    # cover_title, cover_url 같은 것들에 대한 변환. (순서에 주의. 이 구문이 위로 가면 순서가 꼬일 수 있겠음)
    context = re.sub(pattern=r'\[##_cover_([^\]]+)_##\]', repl=r"{{ cover['\g<1>'] }}", string=context,
                     flags=re.MULTILINE)
    # cover 요소에 대한 if 변환
    context = re.sub(pattern=r'<s_cover_([^>]+)>', repl=r"{% if cover['\g<1>'] %}", string=context,
                     flags=re.MULTILINE)
    context = re.sub(pattern=r'</s_cover_([^>]+)>', repl=r'{% endif %}', string=context, flags=re.MULTILINE)
    return context


def parse_index_article_rep(context: str) -> str:
    """
    여기저기 가 있는 s_index_article_rep 를 모아서 s_list 뒷부분에 넣어준다.
    :param context:
    :return:
    """
    s_article_protected = find_tags_inner_html('s_article_protected', context)
    s_index_article_rep = find_tags_inner_html('s_index_article_rep', s_article_protected)
    # s_protected_index = re.findall(r'<s_index_article_rep>.*</s_index_article_rep>', s_protected, re.DOTALL)
    # s_protected_index = s_protected_index[0]

    index_article_rep_protected = "{% if article_rep.is_protected %}" + s_index_article_rep + '\t{% endif %}'
    # print(protected_index_article)

    s_article_rep = find_tags_inner_html('s_article_rep', context)
    s_index_article_rep = find_tags_inner_html('s_index_article_rep', s_article_rep)
    index_article_rep_normal = '{% if article_rep.is_protected is not defined %}' + s_index_article_rep + '{% endif %}'

    # s_list 바로 안쪽 끝에 붙이기. append 하기.
    # contents = re.sub(pattern='</', repl=r'', string=contents, flags=re.MULTILINE)
    index_article_rep_both = "\n\t\t\t\t\t\t{% if article_list_info is defined %}\n\t\t\t\t\t\t" + index_article_rep_protected \
                             + '\n\t\t\t\t\t\t' + index_article_rep_normal + "\n\t\t\t\t\t\t{% else %}"
    # context = context.replace("</s_list>", index_article_both + "</s_list>")

    # index_article_rep 는 s_article_rep의 안에서 앞쪽에 붙는다고 보면 된다...
    context = context.replace("<s_article_rep>", "{% for article_rep in article_index_list %}" + index_article_rep_both)
    context = context.replace("</s_article_rep>", "\t{% endif %}\n\t\t\t\t\t{% endfor %}")

    # 원래 있던 index_article_rep 는 제거하기.
    context = remove_tag('s_index_article_rep', context)

    # article_rep_ 변수들 변환
    context = re.sub(pattern=r'\[##_article_rep_([^\]]+)_##\]', repl=r'{{ article_rep.\g<1> }}', string=context,
                     flags=re.MULTILINE)
    return context


def parse_s_list(context: str) -> str:
    """
    예전 방식의 리스트
    :param context: 
    :return: 
    """
    # s_list 변환
    context = context.replace("<s_list>", "{% if article_list_info is defined %}")
    context = context.replace("</s_list>", "{% endif %}")

    # s_list_empty 변환
    context = context.replace("<s_list_empty>", "{% if article_index_list|length == 0 %}")
    context = context.replace("</s_list_empty>", "{% endif %}")
    
    # s_list_rep 변환
    context = context.replace("<s_list_rep>", "{% for list_rep in article_list_legacy %}")
    context = context.replace("</s_list_rep>", "{% endfor %}")

    # s_list_rep_thumbnail
    context = context.replace("<s_list_rep_thumbnail>", "{% if list_rep.thumbnail %}")
    context = context.replace("</s_list_rep_thumbnail>", "{% endif %}")

    # list_rep_title 같은 변수들 변환
    context = re.sub(pattern=r'\[##_list_rep_([^\]]+)_##\]', repl=r'{{ list_rep.\g<1> }}', string=context,
                     flags=re.MULTILINE)

    # list_conform 같은 변수들 변환. 여기는 info를 이용하므로 article_list_info 로 변환.
    context = re.sub(pattern=r'\[##_list_([^\]]+)_##\]', repl=r'{{ article_list_info.\g<1> }}', string=context,
                     flags=re.MULTILINE)
    return context


def parse_article(context: str) -> str:
    # parmalink_article : 게시글 보기 일 때에 해당하는 사항에 대한 변환.
    # contents = contents.replace("<s_permalink_article_rep>", "{% if article_rep['type'] == 'permalink' %}")
    # contents = contents.replace("</s_permalink_article_rep>", "{% endif %}")
    # 그냥 이 조건문은 제거하기로..
    context = re.sub(pattern=r'</?s_permalink_article_rep>', repl="", string=context,
                     flags=re.MULTILINE)

    # protected article : 보호된 글에 대한 변환.
    context = context.replace("<s_article_protected>", "{% if article_protected %}")
    context = context.replace("</s_article_protected>", "{% endif %}")

    # s_article_rep_ : article의 하위 값들. 작성일, 작성자, 링크, 제목 등
    context = re.sub(pattern=r'<s_article_rep_([^>]+)>', repl=r" {% if article_rep.\g<1> is defined %}", string=context,
                     flags=re.MULTILINE)
    context = re.sub(pattern=r'</s_article_rep_([^>]+)>', repl=r' {% endif %}', string=context, flags=re.MULTILINE)

    # 불필요한 경우들 (작업하려면 봐야하므로)
    context = re.sub(pattern=r'</?s_tag_label>', repl="", string=context, flags=re.MULTILINE)
    context = re.sub(pattern=r'</?s_article_related>', repl="", string=context, flags=re.MULTILINE)
    
    # s_article_rep 변환
    # context = context.replace("<s_article_rep>", "{% if article_rep is defined %}")
    # context = context.replace("</s_article_rep>", "{% endif %}")
    return context


def parse_skin_var(context: str) -> str:
    # 먼저, var 의 dash 방지 (스킨에 따라서 그런 경우가 있길래...)
    context = re.sub(pattern=r'</?s_(if|not)_var_([^>]+)>', repl=lambda m: m.group().replace("-", "_"),
                     string=context, flags=re.MULTILINE)
    context = re.sub(pattern=r'\[##_var_([^\]]+)_##\]', repl=lambda m: m.group().replace("-", "_"),
                     string=context, flags=re.MULTILINE)

    # s_if_var_ 와 s_not_var 를 변환
    # s_if_var 변환
    context = re.sub(pattern=r'<s_if_var_([^>]+)>', repl=r" {% if vars.\g<1> is defined %}", string=context,
                     flags=re.MULTILINE)
    context = re.sub(pattern=r'</s_if_var_([^>]+)>', repl=' {% endif %}', string=context, flags=re.MULTILINE)

    # s_not_var 변환
    # {% if vars.\g<1> is none or not vars['\g<1>'] %}
    context = re.sub(pattern=r'<s_not_var_([^>]+)>', repl=r" {% if vars.\g<1> is not defined %}",
                     string=context, flags=re.MULTILINE)
    context = re.sub(pattern=r'</s_not_var_([^>]+)>', repl=' {% endif %}', string=context, flags=re.MULTILINE)

    # var 출력되는 부분 처리
    context = re.sub(pattern=r'\[##_var_([^\]]+)_##\]', repl=r"{{ vars.\g<1> }}", string=context,
                     flags=re.MULTILINE)
    return context


def parse_notice(context: str) -> str:
    context = re.sub(pattern=r'<s_notice_rep_([^>]+)>', repl=r" {% if notice_rep[\g<1>] %}", string=context,
                     flags=re.MULTILINE)
    context = re.sub(pattern=r'</s_notice_rep_([^>]+)>', repl=r' {% endif %}', string=context, flags=re.MULTILINE)
    return context


def parse_guest(context: str) -> str:
    context = context.replace("<s_guest>", "{% if guest %}")
    context = context.replace("</s_guest>", "{% endif %}")

    # 화면에 보여져야하기 때문에. 몇가지는 그냥 제거
    context = re.sub(pattern=r'</?s_guest_input_form>', repl="", string=context,
                     flags=re.MULTILINE)
    context = re.sub(pattern=r'</?s_guest_member>', repl="", string=context,
                     flags=re.MULTILINE)
    context = re.sub(pattern=r'</?s_guest_container>', repl="", string=context,
                     flags=re.MULTILINE)

    # 변수들
    context = re.sub(pattern=r'\[##_guest_rep_([^\]]+)_##\]', repl=r'{{ guest_rep.\g<1> }}', string=context,
                     flags=re.MULTILINE)
    context = context.replace("[##_guest_name_##]", "방문자이름")
    context = context.replace("[##_guest_input_name_##]", "")
    context = context.replace("[##_guest_input_password_##]", "")
    context = context.replace("[##_guest_password_##]", "")

    context = context.replace("<s_guest_reply_container>", "{% if guest_rep.reply is defined %}")
    context = context.replace("</s_guest_reply_container>", "{% endif %}")

    context = context.replace("<s_guest_reply_rep>", "{% for guest_rep in guest_rep.reply %}")
    context = context.replace("</s_guest_reply_rep>", "{% endfor %}")

    # 불필요한 경우들 (작업하려면 봐야하므로)
    context = re.sub(pattern=r'</?s_guest_form>', repl="", string=context, flags=re.MULTILINE)

    return context


def parse_tag(context: str) -> str:
    context = context.replace("<s_tag>", "{% if route_type == 'tags' %}")
    context = context.replace("</s_tag>", "{% endif %}")

    context = context.replace("<s_tag_rep>", "{% for tag in tags %}")
    context = context.replace("</s_tag_rep>", "{% endfor %}")

    context = context.replace("<s_random_tags>", "{% for tag in tags %}")
    context = context.replace("</s_random_tags>", "{% endfor %}")

    context = context.replace("[##_tag_name_##]", "{{ tag.name }}")
    context = context.replace("[##_tag_link_##]", "{{ tag.link }}")

    # contents = contents.replace("[##_tag_name_##]", "{{ tag_name|safe }}")

    return context


def parse_location_log(context: str) -> str:
    """
    위치 로그 관련
    :param context
    :return: contents
    """
    context = context.replace("<s_local>", "{% if location_log is defined  %}")
    context = context.replace("</s_local>", "{% endif %}")
    return context


def parse_sidebar(context: str) -> str:
    # 화면에 보여져야하기 때문에. 몇가지는 그냥 제거
    context = re.sub(pattern=r'</?s_sidebar>', repl="", string=context,
                     flags=re.MULTILINE)
    context = re.sub(pattern=r'</?s_sidebar_element>', repl="", string=context,
                     flags=re.MULTILINE)
    return context


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
