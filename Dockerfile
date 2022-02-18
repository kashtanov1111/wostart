FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /projects
COPY Pipfile Pipfile.lock /projects/
RUN pip install pipenv && pipenv install --system
COPY . /projects/