FROM python:slim-buster
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY wrapped_driver setup.py README.md MANIFEST.in ./
RUN apt-get update \
 && apt-get upgrade -y \
 # Install packages needed to build
 && apt-get install build-essential libssl-dev libffi-dev rustc -y \
 # Create python egg
 && python setup.py sdist bdist_wheel \
 # Create Virtual Environment
 && python -m venv /wrapped-driver-env \
 # Activate Virtual Environment
 && . /wrapped-driver-env/bin/activate \
 && pip install --upgrade pip \
 # Installing version that can be built on RaspberryPi
 && pip install cryptography==3.4.6 \
 && pip install -e . \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/* \
           __pycache__