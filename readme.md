# 티스토리 스킨 메이커
티스토리 스킨을 만드는데 이용하는 도구입니다. 

스킨 폴더를 생성하여 스킨과 관련된 파일들을 생성하고 작업을 하면 로컬에서 확인을 할 수 있도록 하였습니다.
git에 연결하여 버저닝을 하면서 작업을 하기 편하도록 고려하였습니다.



# 사용법
## 셋팅 방법
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
#### 윈도우 환경 (파이썬 설치 선행 필요)
##### vscode 를 이용할 경우
터미널에서 셋팅하기
```console
python -m venv venv
./venv/scripts/activate
pip install -r requirements.txt
```

flask 실행하기
```console
python -m flask run
```
혹은 vscode터미널에서 준비된 스크립트를 이용해서 flask 실행
```console
runv
```

##### pycharm 을 이용할 경우
파이참의 설정을 통해서 venv셋팅과 pip install을 진행합니다. 혹은 `pip install -r requirements.txt`을 합니다.

pycharm 터미널에서 flask 실행
```console
python -m flask run
```
혹은 pycharm 터미널에서 준비된 스크립트를 이용해서 flask 실행
```console
run
```


## 작성법 및 사용법
skins/ 폴더 밑에 만들고자 하는 스킨 폴더를 생성한다. 해당 스킨 폴더는 개인의 git 저장소로 생성하여 버전 관리를 한다. 

예시
skins/
  - Odyssey 
  - Poster
  - MySkin
  - NewBlogSkin
  - ...

이렇게 각각의 스킨을 만들어서 테스트를 할 수 있다. 

작업을 하게 되면, 'localhost:15000'에 접속시 첫 화면에서 각 스킨에 대한 링크가 생성이 된다. 해당 링크를 누르면, 
스킨에서 태그들을 인식해서 간략하게 웹으로 구현해서 띄워준다. 현재 구현되어 있는 각각의 링크는 다음과 같다.

링크 일람
- `/(스킨 폴더명)/` : 홈 화면
- `/(스킨 폴더명)/category` : 카테고리/글 목록의 화면
- `/(스킨 폴더명)/article` : 게시글 하나가 나오는 화면
- `/(스킨 폴더명)/tags` : 태그 화면 
- `/(스킨 폴더명)/guestbook` : 방명록 화면


# 사용된 파이썬 패키지
* pip install flask : flask
* pip install beautifulsoup4 : html 파싱 관련
* pip install lxml : beautifulsoup4에서 이용
* pip install pytest : test 하는데 이용.

