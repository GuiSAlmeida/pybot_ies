FROM python:3
LABEL maintainer="Guisalmeida"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
CMD python main.py
