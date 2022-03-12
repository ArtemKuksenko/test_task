FROM python:3.10
RUN mkdir -p /opt/app

ADD ./requirements.txt /opt/app
RUN pip3 install -r /opt/app/requirements.txt

ADD ./libs /opt/app/libs
RUN pip3 install /opt/app/libs/run_single_generator

WORKDIR /opt/app

ADD . /opt/app