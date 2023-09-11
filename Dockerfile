FROM python:3.9.18-slim

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash soda && chmod 777 /opt /run

WORKDIR /soda

RUN mkdir /soda/static && mkdir /soda/media && chown -R soda:soda /soda && chmod 755 /soda

COPY --chown=soda:soda . .

RUN pip install -r requirements.txt

USER soda

CMD ["gunicorn","-b","0.0.0.0:8000","AppleStore.wsgi:application"]
