import DataJsonLoader


def test_get_config():
    r = DataJsonLoader.get_blog_config_json()
    print(r['title'])
