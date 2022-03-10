FROM python:3.10
RUN mkdir -p /opt/app

ADD ./requirements.txt /opt/app
RUN pip3 install -r /opt/app/requirements.txt

WORKDIR /opt/app

ADD . /opt/app