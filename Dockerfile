FROM python:3.7-slim-buster
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY wrapped_driver setup.py README.md MANIFEST.in ./
RUN apt-get update \
 && apt-get upgrade -y \
 # Create python egg
 && python setup.py sdist bdist_wheel \
 && pip install -e . \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/* \
           __pycache__