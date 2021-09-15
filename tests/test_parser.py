import SkinLoader
import re
from bs4 import BeautifulSoup


def test_render_skin():
    SkinLoader.render_skin('skin-bookclub-custom')


def test_parse_index_article_rep():
    skin_law = SkinLoader.get_skin_raw('skin-bookclub-custom')


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
