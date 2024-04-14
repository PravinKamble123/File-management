# Use the Python 3.9 image based on Alpine Linux 3.13
FROM python:3.10-alpine

# Set the maintainer label
LABEL maintainer="pravin kamble"

# Set the environment variable to prevent buffering of Python output
ENV PYTHONUNBUFFERED 1

# Copy the requirements files and the app code into the container
COPY ./requirements.txt /tmp/requirements.txt

COPY . /app

# Set the working directory to /app
WORKDIR /app

# Expose port 8001 (assuming your app listens on this port)
EXPOSE 8001

# Define an ARG for the DEV flag (default is false)
ARG DEV=false

# Install dependencies and create a virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \  
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Add the virtual environment's bin directory to the PATH
ENV PATH="/py/bin:$PATH"

# Switch to the django-user as the default user for running the container
USER django-user