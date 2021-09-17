# 티스토리 스킨 시뮬레이터
티스토리 스킨을 로컬에서 돌려볼 수 있습니다. 

로컬 환경을 구성하면 스킨은 별도의 본인 git 저장소에 관리를 할 수 있게 됩니다. 

아직 기능이 완벽하지는 않으나, 간단한 형태로는 구현할 수 있게 되었습니다.

<br><br><br>
# 1. 라이선스
제가 이용하고자 만들었으나, 필요하신 분이 계실까 하여 MIT 라이선스로 관리하기로 하였습니다. 

수정이 필요한 부분이 있으시면, fork 하셔서 맘편하게 수정을 하시면 되겠습니다. 

<br><br><br>
# 2. 사용법
## 2.1. 셋팅 방법
### 방법1. 도커 이용하기 
```console
docker build -t tistory-skin-local .
docker run --name tistory-skin-local -d -p 15000:5000 -v "%cd%:/app" tistory-skin-local
```

### 방법2. 도커 컴포즈 이용하기
명령어가 조금 더 간단합니다.

```console
docker-compose up --build --force-recreate -d
```

### 방법3. 도커없이 그냥 flask 구동하기
#### 윈도우 환경 (파이썬 설치 선행 필요: 파이썬 3 이상 필요)
1. 다운로드 받거나 git clone 하기. 
    `git clone https://github.com/exizt/tistory-skin-simulator.git`
2. 셋팅 : 해당 폴더에 있는 `install.bat`을 더블클릭하여 실행하거나, 해당 경로에서 커맨드창을 열고 실행하기
   - install.bat을 사용하지 않고 터미널창(커맨드창)에서 직접 명령줄을 실행해도 됨. 
   - venv 만들고, pip install 하시면 됩니다.
3. flask 실행 : 해당 폴더에 있는 `run.bat`을 더블클릭하여 실행하거나, 터미널창에서 실행

<br><br><br>
## 2.2. 작성법 및 사용법
**요약**
1. skins/ 폴더 밑에 만들고자 하는 스킨 폴더를 생성합니다. skins 이하는 이곳 git에 포함이 되지 않도록, gitignore 설정이 되어 있습니다.
2. skins 밑에 본인의 스킨 폴더를 새로 만드시고 git 저장소로 관리하시면 됩니다. 
3. flask 를 실행하시면 `localhost:15000`으로 접속하여 확인하실 수 있습니다.

### 스킨 만들기
1. `skins` 폴더 및에 만들고자 하는 스킨 폴더를 생성합니다.
2. 해당 폴더는 별도의 git 저장소로 관리하거나 편하시대로 이용하시면 됩니다. 
3. 에디터는 편하신 대로 사용하시면 됩니다...


skins 폴더 구성 예시)
```text
skins/
  - Odyssey : 다른 곳에서 복사해온 스킨
  - Poster : 다른 곳에서 복사해온 스킨
  - MySkin : 작업중인 스킨 예시. 별도의 git 저장소로 관리해도 됨.
  - NewBlogSkin : 작업중인 스킨 예시. 별도의 git 저장소로 관리해도 됨.
  - ...
```
이렇게 제각각 다른 폴더로 구성을 할 수 있게 되어 있습니다. 

필수적으로 생성해야 하는 스킨 내의 파일
1. index.xml : 내부의 default 값이나 variables 를 로드하기 때문에 필요로 합니다. 
2. skin.html : 작업하실 스킨 파일.

### 접속하기, 시뮬레이션 보기 
1. `run.bat`을 더블 클릭 혹은 실행시켜서, flask 웹서버를 실행
2. 웹브라우저에서 `localhost:15000` 으로 접속하면 스킨 폴더 목록이 나옴.
3. 해당 스킨폴더이름을 클릭
 

지원되는 링크 일람
- `/` : 스킨을 선택하는 화면. 매우 단순하게 되어있고, 해당 스킨을 선택하면 됩니다. 
- `/(스킨 폴더명)/` : 홈 화면
- `/(스킨 폴더명)/category` : 카테고리/글 목록의 화면
- `/(스킨 폴더명)/article` : 게시글 하나가 나오는 화면
- `/(스킨 폴더명)/tags` : 태그 화면 
- `/(스킨 폴더명)/guestbook` : 방명록 화면

<br><br><br>
# 3. 코드에 대한 간략 설명
거의 대부분은 정규표현식으로 replace 하는 형태로 되어있습니다. 

동작은 해당 스킨의 url (`/(스킨폴더명)/`)으로 접속시 해당 스킨에 대해서, flask에서 이용할 수 있도록 templates 파일을 생성합니다. 

생성되는 파일은 `templates/skin_cache/` 밑에 위치합니다. 

변경이 잘 안 될 시에는 이 폴더에 있는 임시 templates파일들(`스킨폴더명_skin.html`로 생성됨)을 삭제하시고 새로고침하시면 됩니다. 
<br><br><br>

# 사용된 파이썬 패키지
* pip install flask : flask
* pip install beautifulsoup4 : html 파싱 관련
* pip install lxml : beautifulsoup4에서 이용
* pip install pytest : test 하는데 이용.


# 연관 키워드, 연관 태그
티스토리 스킨 만들기, 티스토리 스킨 가이드, 티스토리 스킨 제작, 티스토리 스킨 메이커, 티스토리 스킨 빌더, 티스토리 스킨 시뮬레이터
