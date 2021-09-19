import os
import pathlib
import SkinParser


def get_skins() -> list:
    """
    스킨 목록을 조회
    :return:list:스킨 목록
    """
    # skins 디렉토리의 경로
    skins_path = get_skins_dir_path()
    # skin의 목록
    # skins = os.listdir(skins_path)
    skins = [name for name in os.listdir(skins_path) if os.path.isdir(os.path.join(skins_path, name))]
    if len(skins) > 0:
        return skins
    else:
        return []


def get_skin_html_path(skin_name: str):
    """
    현재 스킨의 skin.html 의 절대경로를 가져오는 기능
    :param skin_name:
    :return:
    """
    skin_path = get_skin_path(skin_name)
    html_path = os.path.join(skin_path, 'skin.html')
    return html_path


def get_skin_path(skin_name: str) -> str:
    """
    선택된 skin_name에 해당하는 디렉토리의 절대 경로를 가져오는 기능
    :param skin_name: 
    :return: 
    """
    skins_dir = get_skins_dir_path()
    skin_path = os.path.join(skins_dir, skin_name)
    return skin_path


def get_skins_dir_path() -> str:
    """
    skins 디렉토리의 절대 경로를 가져오는 기능
    :return: skins 디렉토리의 절대 경로
    """
    # skins 디렉토리의 경로
    skins_path = os.path.join(get_current_path(), 'skins')
    return skins_path


def get_current_path():
    """
    현재 파일의 절대 경로를 가져오는 기능
    :return:obj:현재 파일의 절대 경로
    """
    # 현재 파일의 경로
    return pathlib.Path(__file__).parent.absolute()


def read_skin_raw(skin_name: str) -> str:
    """
    스킨(skin.html)의 내용을 가져오는 기능
    :param skin_name: 스킨 폴더의 이름
    :return: 스킨의 내용
    """
    with open(get_skin_html_path(skin_name), 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents


def get_skin_mtime(skin_name):
    """
    skin.html 의 최근변경시간을 가져오는 기능
    :param skin_name: 
    :return: 
    """
    return os.path.getmtime(get_skin_html_path(skin_name))


def get_templates_cache_dir_path():
    """
    skin 템플릿 디렉토리의 경로
    :return:
    """
    path = os.path.join(get_current_path(), 'templates')
    path = os.path.join(path, 'skin_cache')
    return path


def get_template_file_name(skin_name):
    """
    생성된 flask 템플릿 파일의 이름 지정.
    :param skin_name: 스킨폴더명
    :return: (skin_name)_skin.html
    """
    return f'{skin_name}_skin.html'


def get_template_file_path(skin_name):
    """
    생성된 flask 템플릿 파일의 절대 경로
    :param skin_name: 
    :return: flask 템플릿 파일의 절대 경로
    """
    path = get_templates_cache_dir_path()
    path = os.path.join(path, get_template_file_name(skin_name))
    return path


def get_template_file_relpath(skin_name):
    """
    생성된 skin 템플릿 파일의 상대 경로
    정확히는 'templates/' 이후의 경로
    :param skin_name: 
    :return: 
    """
    return 'skin_cache/' + get_template_file_name(skin_name)


def get_template_file_mtime(skin_name):
    """
    생성된 템플릿 파일의 최근 변경 시간 조회
    :param skin_name: 
    :return: 
    """
    return os.path.getmtime(get_template_file_path(skin_name))


def to_template(skin_name):
    """
    스킨 내용을 로드해서 flask template 형태로 변환해서 저장하는 기능
    :param skin_name: 
    :return: 
    """
    # skin.html의 내용을 로드
    context = read_skin_raw(skin_name)

    # template 형태로 렌더링
    context = SkinParser.parse(context)

    # 템플릿 파일로 생성
    with open(get_template_file_path(skin_name), 'w', encoding='utf-8') as f:
        f.write(context)
