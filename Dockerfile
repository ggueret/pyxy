FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
ADD requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt
ADD . /usr/src/app/

ENV PYXY_CACHE_DIR /data

EXPOSE 80
VOLUME /data
WORKDIR /usr/src/app
CMD ["gunicorn", "--worker-class=gevent", "--bind=0.0.0.0:80", "pyxy:app"]
