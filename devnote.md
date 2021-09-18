# 개발 관련 노트


# 셋팅 (고급자)

명령어로 git clone부터 하나씩

## 윈도우 환경 
(셋팅) 한줄씩 실행.
```console
git clone https://github.com/exizt/tistory-skin-simulator.git tistory-skin-simulator
cd tistory-skin-simulator
python -m venv venv
call venv/scripts/activate
pip install -r requirements.txt
```

(실행)
```console
call venv/scripts/activate
python -m flask run
```


## 리눅스 환경
(셋팅) 한줄씩 실행.
```console
git clone https://github.com/exizt/tistory-skin-simulator.git tistory-skin-simulator
cd tistory-skin-simulator
python -m venv venv
./venv/scripts/activate
pip install -r requirements.txt
```

(실행)
```console
./venv/scripts/activate
python -m flask run
```

## pycharm
pycharm 에디터의 터미널을 이용할 경우는, venv나 pip install하는 부분 없이 설정을 통해서 하시면 됩니다. 
자동으로 잘 안 잡히신다면.. 마찬가지로 명령어를..



