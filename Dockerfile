# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Add Postgres apt repository so you can get version 16...
RUN apt-get update
RUN apt-get install curl ca-certificates -y && \
    install -d /usr/share/postgresql-common/pgdg && \
    curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc && \
    sh -c 'echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Install dependencies
RUN apt-get update
RUN apt-get install \
    gcc \
    python3-dev \
    python3-setuptools \
    libgdal32 \
    libpq-dev \
    postgresql-server-dev-all \
    libjpeg-turbo-progs \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libopenjp2-7-dev \
    netcat-traditional -y

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

RUN mkdir static && \
    mkdir media && \
    mkdir logs && \
    mkdir backups && \
    cp memorymap_toolkit/settings/secret_settings_template.py memorymap_toolkit/settings/secret_settings.py

RUN chmod +x entrypoint.sh

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "memorymap_toolkit.wsgi"]
