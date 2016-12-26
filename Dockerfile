FROM python:2.7-alpine

RUN apk add --no-cache --virtual .build-deps gcc musl-dev && pip install setuptools==0.6c11 && pip install Twisted==10.1.0 && apk del .build-deps

COPY . /app/

WORKDIR /app

RUN python setup.py install
ENV user=user pass=pass

EXPOSE 110 25

CMD twistd --nodaemon singlemailboxserver --pop3port=110 --smtpport=25  --pop3username=${user} --pop3password=${pass} --smtplisten=0.0.0.0
