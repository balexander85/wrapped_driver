FROM python:buster
ARG build_dependencies="build-essential libssl-dev libffi-dev"
# need env var ERROR: Could not build wheels for cryptography
#ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /app
COPY wrappeddriver.py requirements.txt __init__.py setup.py README.md MANIFEST.in ./
RUN apt-get update \
 && apt-get upgrade -y \
 # Install packages needed to build
 && apt-get install $build_dependencies -y \
 # Create python egg
 && python setup.py sdist bdist_wheel \
 # Create Virtual Environment
 && python -m venv /wrapped-driver-env \
 # Activate Virtual Environment
 && . /wrapped-driver-env/bin/activate \
 && pip install --upgrade pip \
 # Installing version that can be built on RaspberryPi
# && pip install cryptography==3.1.1 \
 && pip install -e . \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
                  $build_dependencies \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*
