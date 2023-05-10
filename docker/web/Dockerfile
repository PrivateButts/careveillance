FROM python:3.11-slim-bullseye AS build-venv

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/careveillance

# Update the system and install dependencies
RUN apt-get update && apt-get -y upgrade


# Copy Pipfile
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

# install pipenv
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir pipenv

# Freeze requirements
RUN pipenv requirements > requirements.txt

# Create Virtualenv and Install
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim-bullseye AS server

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV GUNICORN_WORKERS=4

WORKDIR /usr/src/careveillance

# Update the system and install dependencies
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install netcat

# Copy virtualenv
COPY --from=build-venv /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# copy project
COPY . .

RUN chmod +x /usr/src/careveillance/docker/web/entrypoint.sh

ENTRYPOINT ["sh", "/usr/src/careveillance/docker/web/entrypoint.sh"]
CMD [ "sh", "-c", "gunicorn -b 0.0.0.0:8000 -w $GUNICORN_WORKERS careveillance.wsgi:application" ]
