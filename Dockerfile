# Reference from https://github.com/raccoonyy/django-sample-for-docker-compose
FROM python:3.7.3
MAINTAINER mnhan0403@gmail.com

RUN apt-get update && apt-get -y install \
    libpq-dev

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project
COPY ./sp_server /app/sp_server

# Copy app
COPY ./processing /app/processing
COPY ./manage.py /app/

# Start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
