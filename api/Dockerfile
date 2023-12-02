FROM python:3.9

ARG APPENV=prod

ENV DJANGO_SETTINGS_MODULE=drfboilerplate.settings.${APPENV}

WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
RUN mkdir static
COPY . /code/

EXPOSE 8001

CMD gunicorn --bind=0.0.0.0:8001 --timeout=10 drfboilerplate.wsgi:application -k gevent --log-level=debug
