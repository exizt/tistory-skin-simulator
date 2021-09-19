import os
import pathlib
import json
import time
import copy

# 프로젝트 루트의 경로
PATH_PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()

# DATA 폴더의 경로
PATH_DATA_DIR = os.path.join(PATH_PROJECT_ROOT, 'data')
PATH_DATA_CUSTOM_DIR = os.path.join(PATH_PROJECT_ROOT, 'data_custom')

# 불러온 데이터를 메모리에 캐싱
DATA_CACHED = {}
DATA_CACHED_TIME = {}


def get_blog_config_json():
    return get_data_json('config.json')


def get_articles():
    return get_data_json('articles.json')


def get_data_json(file_name):
    """
    data/ 폴더에서 해당하는 이름의 json 파일의 데이터를 로드.
    :param file_name:
    :return:
    """
    path = os.path.join(PATH_DATA_DIR, file_name)
    custom_path = os.path.join(PATH_DATA_CUSTOM_DIR, file_name)

    # 커스텀 데이터 설정이 있는 경우, 그것으로 대체
    if os.path.exists(custom_path):
        path = custom_path

    if file_name not in DATA_CACHED:
        DATA_CACHED[file_name] = get_json(path)
        DATA_CACHED_TIME[file_name] = time.time()
        print(f'load blog data..(/data/{file_name})')
    else:
        if file_name in DATA_CACHED_TIME:
            changed_at = os.path.getmtime(path)
            if changed_at > DATA_CACHED_TIME[file_name] + 1:
                # 재생성
                print(f'Detected change in (/data/{file_name}), reloading..')
                DATA_CACHED[file_name] = get_json(path)
                DATA_CACHED_TIME[file_name] = changed_at

    # 깊은 복사를 해야할 듯?
    return copy.deepcopy(DATA_CACHED[file_name])
    # return DATA_CACHED[file_name]


def get_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # context = f.read()
        context = json.load(f)
    return context
