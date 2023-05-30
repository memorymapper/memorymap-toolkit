# Use an official Python runtime as the base image
FROM python:3.10.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        binutils \
        gcc \
        gdal-bin \
        libproj-dev \
        libpq-dev \
        musl-dev \
        memcached \
        netcat \
        python3-dev

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /code/
RUN chmod +x entrypoint.sh

# Copy the Django project code into the container
COPY . /code/

# Make the logs, media and static directories
RUN mkdir /code/logs/ &&\
    mkdir /code/media/ &&\
    mkdir /code/static/

# Expose the port that Django will run on (default is 8000)
EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

# Run Django migrations and collect static files
#RUN python manage.py makemigrations --no-input --settings=memorymap_tookit.#settings.local
#RUN python manage.py migrate --no-input --settings=memorymap_tookit.settings.#local
#RUN python manage.py collectstatic --no-input --settings=memorymap_tookit.#settings.local

# Set the default command for the container
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "memorymap_toolkit.wsgi:application"]
