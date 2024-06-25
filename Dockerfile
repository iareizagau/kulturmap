# syntax=docker/dockerfile:1
FROM python:3.11
RUN apt-get -y update \
    && apt-get install -y \
    redis-server \
    && apt-get -y clean

# Diasbles generation of pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# stdout and stderr streams are not buffered and sent straight to your terminal
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/opendataeuskadi
ENV LOG_HOME=$APP_HOME/logs
# ENV APP_USER=appuser

RUN mkdir $APP_HOME
RUN mkdir $LOG_HOME
RUN mkdir -p $LOG_HOME/celery
RUN mkdir -p $LOG_HOME/redis

WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip uninstall -y django-allauth
RUN pip install django-allauth

COPY . /opendataeuskadi/
# COPY supervisord.conf /etc/supervisor/supervisord.conf

# RUN python manage.py collectstatic --no-input

# Creating the user
# RUN addgroup --system dockeruser && adduser --system --group dockeruser
    # echo "dockeruser ALL=(ALL) NOPASSWD: /usr/bin/redis-server" >> /etc/sudoers

# Changing ownership of all files and folders in work dir to user
# RUN chown -R dockeruser:dockeruser $APP_HOME $LOG_HOME $LOG_HOME/redis
# RUN chown /var/lib/redis
# RUN chmod -R 770 /var/lib/redis

# RUN sed -i 's/^supervised.*/supervised systemd/' /etc/redis/redis.conf
# RUN sed -i 's/^user.*/user dockeruser/' /etc/redis/redis.conf
# RUN sed -i 's/^group.*/group dockeruser/' /etc/redis/redis.conf

# Changing to user
# USER dockeruser

CMD service redis-server start & \
    celery -A OpenDataEuskadi beat --loglevel=info & \
    celery -A OpenDataEuskadi worker --loglevel=info  & \
    gunicorn --bind 0.0.0.0:8000 OpenDataEuskadi.wsgi:application