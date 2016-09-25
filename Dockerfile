# use tensorflow as base image
FROM gcr.io/tensorflow/tensorflow:latest-devel

MAINTAINER Ricardo Lobo <ricardolobo@lcdporto.org>

# update repos and install dependencies
RUN apt-get update && \
apt-get -y install \
python-pip \
python-dev

ADD . /app
WORKDIR /app

RUN mkdir /uploads

RUN pip install -r requirements.txt

EXPOSE 80

RUN groupadd -r apprunner
RUN useradd -r -g apprunner -d / -s /usr/sbin/nologin -c "Docker image user" apprunner

CMD ["gunicorn","-b","0.0.0.0:80","-w","3","-k","gevent","--log-file","-","--log-level","debug","--access-logfile","-","api:app"]