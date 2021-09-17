FROM python:3.9.6-slim-buster
WORKDIR /app

COPY requirements.txt .

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

# pip 의존성 설치
RUN pip install -r requirements.txt

ENTRYPOINT python -m flask run --host=0.0.0.0 --port=5000