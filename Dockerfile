FROM python:3.6.7-alpine3.7

RUN mkdir -p /opt/gaf3

WORKDIR /opt/gaf3

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD lib lib
ADD test test

ADD setup.py .

ENV PYTHONPATH "/opt/gaf3/lib:${PYTHONPATH}"
