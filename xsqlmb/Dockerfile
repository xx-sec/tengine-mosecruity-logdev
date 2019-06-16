FROM python:3.6

ADD . /usr/local/xsqlmb
WORKDIR /usr/local/xsqlmb
RUN cd /usr/local/xsqlmb && pip install -r requirements.txt

USER root 
CMD ['python3']

