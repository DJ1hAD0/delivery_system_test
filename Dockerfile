FROM python:3.11


RUN mkdir /fastapi_app

WORKDIR  /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY init_conf.sh /docker-entrypoint-initdb.d/

COPY app.sh /fastapi_app/

COPY . .

RUN chmod a+x *.sh



