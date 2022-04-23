# run celery
FROM python:3.6 AS celery
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir /app/tmp
WORKDIR /app
RUN apt update && apt-get -y install ffmpeg postgresql-client
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app/

#settings
RUN mv ./backend/settings.py ./backend/_settings.py
RUN cat ./backend/_settings.py | sed  "s/'REDIS', 'localhost'/'REDIS', 'redis'/" > ./backend/settings.py

#local.py
RUN cat ./backend/_local.py | sed  "s/'POSTGRES_HOST', 'localhost'/'POSTGRES_HOST', 'postdb'/" > ./backend/__local.py
RUN cat ./backend/__local.py | sed  "s/localhost:8888/socket:8889/" > ./backend/local.py

#socket
RUN mv socket_server.py __socket_server.py
RUN cat __socket_server.py | sed  -e "s/redis:\/\/localhost/redis:\/\/redis/" > _socket_server.py
RUN cat _socket_server.py | sed  -e "s/Redis(host='localhost'/Redis(host='redis'/" > socket_server.py
#CMD ["celery -A backend worker -l info"]

# run seeddb
FROM celery as seeddb
WORKDIR /app

# run beat
FROM celery as beat
WORKDIR /app
#CMD ["celery -A backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler"]

# run socket
FROM celery as socket
WORKDIR /app
#CMD ["python", 'socket_server.py']

# run django
FROM celery as django
WORKDIR /app
#CMD ["python manage.py runserver 8085"]
