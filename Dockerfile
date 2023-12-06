FROM python:3.10.13-slim


ENV TZ Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone


RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    libpq-dev gnupg lsb-release debconf-utils gcc g++ locales \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
 && truncate -s 0 /var/log/*log

RUN echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen \
 && locale-gen
ENV LANGUAGE=ru_RU.UTF-8 LANG=ru_RU.UTF-8 LC_ALL=ru_RU.UTF-8

RUN groupadd -g 1000 web \
 && useradd -m --no-log-init -r -g 1000 -u 1000 web
USER web

ENV HOME=/home/web
ENV APP_HOME=$HOME/app
ENV PYTHONUSERBASE=$HOME/packages VIRTUAL_ENV=$HOME/.venv
ENV PATH=$PYTHONUSERBASE/bin:$VIRTUAL_ENV/bin:$PATH
RUN mkdir /home/web/app
WORKDIR $APP_HOME

RUN pip completion --bash >> /home/web/.bashrc \
 && python3 -m venv $VIRTUAL_ENV \
 && pip install --user poetry==1.7.0

COPY --chown=web:web pyproject.toml poetry.lock ./
RUN poetry install

COPY --chown=web:web . .
