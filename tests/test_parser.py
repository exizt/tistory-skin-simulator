import SkinLoader
import re
from bs4 import BeautifulSoup

import SkinParser
import SkinController


def test_render_skin():
    SkinLoader.to_template('skin-bookclub-custom')


def my_replace(match):
    print(match.group())
    return match.group().replace("-", "_")


def test_replace_menu():
    context = SkinController.get_blog_config_json()
    blog_menu = context['blog_menu']
    # print(blog_menu)
    skin_name = 'custom-asdd'
    blog_menu = re.sub(pattern=r'<a href="/([^"]*)"', repl=r'<a href="/'+skin_name+r'/\g<1>"',
                       string=blog_menu,
                       flags=re.MULTILINE)
    print(blog_menu)


def test_dash_to_underscore2():
    # 다양한 상황이 존재한 경우
    contents = """
    <s_if_var_promotion-1-image>
    <s_if_var_promotion-1-text>
    <span class="text"<s_if_var_promotion-1-color> style=color:[##_var_promotion-1-color_##]
    </s_if_var_promotion-1-color>>
        [##_var_promotion-1-text_##]
    </span>
    """
    # contents = re.sub(pattern=r'vars\.([a-z]+?)\-([a-z]+?)', repl=r'vars.\g<1>_\g<2>', string=contents,
    #                  flags=re.MULTILINE)
    # contents, num = re.subn(pattern=r'vars\.(.+?)', repl=lambda m: m.group().replace("-", "_"), string=contents,
    #                        flags=re.MULTILINE)
    contents, num = re.subn(pattern=r'</?s_if_var_([^>]+)>', repl=lambda m: m.group().replace("-", "_"), string=contents,
                            flags=re.MULTILINE)
    contents, num = re.subn(pattern=r'\[##_var_([^\]]+)_##\]', repl=lambda m: m.group().replace("-", "_"), string=contents,
                            flags=re.MULTILINE)
    print(contents)
    # print(num)

    # regex = re.compile('vars.([a-z]-[a-z])', re.S)
    # contents = regex.sub(lambda m: m.group().replace('-', "_"), contents)
    # print(contents)

def test_dash_to_underscore():
    contents = """
    vars.a-z-b
    vars.add-zee
    vars.zddd-eeee-ddcc
    """
    # contents = re.sub(pattern=r'vars\.([a-z]+?)\-([a-z]+?)', repl=r'vars.\g<1>_\g<2>', string=contents,
    #                  flags=re.MULTILINE)
    # contents, num = re.subn(pattern=r'vars\.(.+?)', repl=lambda m: m.group().replace("-", "_"), string=contents,
    #                        flags=re.MULTILINE)
    contents, num = re.subn(pattern=r'vars\.[a-z_-]*', repl=my_replace, string=contents,
                            flags=re.MULTILINE)
    print(contents)
    # print(num)

    # regex = re.compile('vars.([a-z]-[a-z])', re.S)
    # contents = regex.sub(lambda m: m.group().replace('-', "_"), contents)
    # print(contents)


def test_render_index_article():
    contents = SkinLoader.read_skin_raw('skin-bookclub-custom')

    # print(contents)
    # ss = re.findall(r'<s_article_protected>(.+?)</s_article_protected>', contents, re.MULTILINE)
    # ss = re.findall(r'<s_article_protected>.*</s_article_protected>', contents, re.DOTALL)
    # ss = re.search(pattern=r'<s_article_protected>(.*?)</s_article_protected>', string=contents)
    # s_protected = ss[0]
    s_article_protected = SkinParser.find_tags_inner_html('s_article_protected', contents)
    s_index_article_rep = SkinParser.find_tags_inner_html('s_index_article_rep', s_article_protected)
    # s_protected_index = re.findall(r'<s_index_article_rep>.*</s_index_article_rep>', s_protected, re.DOTALL)
    # s_protected_index = s_protected_index[0]

    index_article_protected = '{% if protected %}' + s_index_article_rep + '{% endif %}\n'
    # print(protected_index_article)

    s_article_rep = SkinParser.find_tags_inner_html('s_article_rep', contents)
    s_index_article_rep = SkinParser.find_tags_inner_html('s_index_article_rep', s_article_rep)
    index_article_normal = '{% if not protected %}' + s_index_article_rep + '{% endif %}\n'

    # s_list 바로 안쪽 끝에 붙이기. append 하기.
    # contents = re.sub(pattern='</', repl=r'', string=contents, flags=re.MULTILINE)
    contents = contents.replace("</s_list>", index_article_protected + index_article_normal + "</s_list>")

    # 원래 있던 protected index_article_rep 는 제거하기.
    # contents = SkinParser.remove_tag('s_index_article_rep', contents)

    print(contents)


def test_find_tags_inner_html():
    """
    SkinParser.find_tags_inner_html 의 기능 테스트
    :return: None
    """
    s = """
    <a>가나다라
    <span>dddd</span>
    </a>"""

    r = SkinParser.find_tags_inner_html('a', s)
    # print(r)
    assert r == """가나다라
    <span>dddd</span>
    """


def test_remove_by_tags_direct():
    contents = """
    <a>가나다라
    <span>dddd</span>
    </a>
    <h1>abcd</h1>
    <a>가나다라
    <span>dddd</span>
    </a>
    """
    # regex = r'<a>.*</a>'
    # contents = re.sub(pattern=regex, repl='', string=contents, flags=re.DOTALL)
    # regex = r'<a>.*[\n]+.*</a>'
    regex = r'<a>.+?</a>'
    contents = re.sub(pattern=regex, repl='', string=contents, flags=re.DOTALL)
    print('\n==========')
    print(contents)
    print('==========')


def test_remove_by_tags():
    contents = """
    <a>가나다라
    <span>dddd</span>
    </a>
    """
    contents = SkinParser.remove_tag('a', contents)
    print('\n==========')
    print(contents)
    print('==========')


def test_parse_index_article_rep():
    skin_law = SkinLoader.read_skin_raw('skin-bookclub-custom')
    soup = BeautifulSoup(skin_law, "lxml")
    s = soup.find_all("s_index_article_rep")

    result = ''
    for i in s:
        # print(i.parent.name)
        parent_name = i.parent.name
        if parent_name == 's_article_protected':
            # print(type(i))
            result += "{% if protected %}\n" + str(i)
            result += "{% endif %}"
        elif parent_name == 's_article_rep':
            result += "{% if not protected %}\n" + str(i)
            result += "{% endif %}"

    print(result)
    # result 를 s_list 끝에 붙여야 함..
    # s_list = soup.find_all("s_list")
    # s_list.insert(0, NavigableString(result))

    # print(soup)


def test_render_var_if():
    str_1 = """
    <s_if_var_logo>aaa</s_if_var_logo>
    <s_if_var_promotion-1-image>bbb</s_if_var_promotion-1-image>
    """
    # str_1 = str_1.replace('')

    # rec = re.compile(r'<s_if_var_[^>]+>')

    # result = rec.sub(r'\1', str_1)
    # result = re.sub(pattern=r'<s_if_var_(.+)>$', repl=r'\g<1>', string=str_1, flags=re.MULTILINE)
    result = re.sub(pattern=r'<s_if_var_([^>]+)>', repl=r'{% if \g<1> %}', string=str_1, flags=re.MULTILINE)
    result = re.sub(pattern=r'</s_if_var_([^>]+)>', repl='{% endif %}', string=result, flags=re.MULTILINE)

    print(result)
