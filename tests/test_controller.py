import SkinLoader
import re
from bs4 import BeautifulSoup
import SkinController
import json


def test_get_config():
    r = SkinController.get_blog_config_json()
    print(r['title'])
