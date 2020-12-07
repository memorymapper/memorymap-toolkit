#########
# BUILD #
#########
FROM debian:buster-slim as build
ENV	PYTHONDONTWRITEBYTECODE 1 
ENV	PYTHONUNBUFFERED 1 
ENV MEMORYMAPPER_VERSION="master" \
		HOME=/home/app \
		APP_HOME=/home/app/web \
		PACKAGES="python3-pip python3-venv postgresql postgresql-contrib postgis python3-dev libpq-dev" \
		DEBIAN_FRONTEND="noninteractive"
RUN apt-get update \
		&& apt-get install -y $PACKAGES \
		&& mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN pip3 install --upgrade pip  \
		&& pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt \
		&& pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels install gunicorn
#########
# Final #
#########
FROM debian:buster-slim 
ENV HOME=/home/django-data \
		DEBIAN_FRONTEND="noninteractive"
RUN groupadd -r --gid 295 django-data \ 
		&& adduser --home $HOME --disabled-password --uid 295 --gid 295 --gecos "" django-data 
WORKDIR $HOME
COPY --from=build /usr/src/app .
COPY docker_settings.py  memorymap_toolkit/settings/secret_settings.py
RUN apt-get -y update \
		&& apt-get install --no-install-recommends -y python3-pip libpq5 python3-gdal \
		&& apt-get clean autoclean \
		&& apt-get autoremove --yes \
		&& rm -rf /var/lib/{apt,dpkg,cache,log}/ \
		&& pip3 install --no-cache $HOME/wheels/* \
		&& rm -rf wheels \
		&& mkdir media \
		&& ln -s /dev/stdout ./logs \
		&& chown -R django-data:django-data $HOME
USER 295
CMD /usr/bin/sh ; sleep infinity
