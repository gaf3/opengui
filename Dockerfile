FROM python:3.6.7-alpine3.7

RUN mkdir -p /opt/service

WORKDIR /opt/service

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD opengui.py .
ADD test_opengui.py .
ADD setup.py .

ENV PYTHONPATH "/opt/service/lib:${PYTHONPATH}"
