FROM python:3.11


RUN mkdir /fastapi_app

WORKDIR  /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.sh /docker-entrypoint-initdb.d/

COPY . .

RUN chmod a+x *.sh



