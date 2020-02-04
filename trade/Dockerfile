
FROM python:3.8
ENV PYTHONUNBUFFERED 1

VOLUME /trade:/trade
WORKDIR /trade

# Installing OS Dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev

RUN pip install -U pip setuptools

COPY requirements.txt /trade/
COPY requirements-opt.txt /trade/

RUN pip install -r /trade/requirements.txt
RUN pip install -r /trade/requirements-opt.txt

ADD .. /trade/

# Django service
EXPOSE 8000