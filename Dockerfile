# pull official base image
FROM python:3.7.9-slim

# set work directory
WORKDIR /usr/src/scaffold

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE project.settings.settings
# install dependencies
RUN apt-get update \
&& apt-get install gcc libjpeg-dev libpq-dev zlib1g-dev python3-dev musl-dev git-all -y \ 
&& apt-get clean
RUN pip install pip-tools

# copy project
COPY . .

#COPY ./requirements/local.txt ./requirement/local.txt
RUN pip-sync requirements/local.txt