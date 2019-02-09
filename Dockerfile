# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.

# FROM python:alpine

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=service Version=0.0.1
EXPOSE 3000

# WORKDIR /app

FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /app
WORKDIR /app
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

# # Using pip:
# RUN python3 -m pip install -r requirements.txt
# CMD ["python3", "-m", "service"]

# Using pipenv:
# RUN python3 -m pip install pipenv
# RUN python3 pipenv install
# RUN python3 pipenv shell
# RUN python3 manage.py runserver
# CMD ["pipenv", "run", "python3", "-m", "service"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m service"
