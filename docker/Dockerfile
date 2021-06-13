FROM python:3.9.5-buster

RUN apt-get update && \
    apt-get install nginx -y

RUN rm /etc/nginx/sites-enabled/default

COPY nginx/nginx.conf /etc/nginx/sites-enabled

WORKDIR /app

COPY . /app

RUN rm .env*

RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r /app/requirements.txt && \
    /venv/bin/pip install --no-cache-dir uwsgi gevent

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV /venv

ENV PATH $VIRTUAL_ENV/bin:$PATH

EXPOSE 80

CMD ["./start_server.sh"]
