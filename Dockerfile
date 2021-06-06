FROM python:3.7-slim-buster
ARG geckodriver_ver=0.29.0
ARG build_dependencies="git curl bzip2"
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY . .
RUN apt-get update \
 && apt-get upgrade -y \
 # Install tools for building
 && pythonDeps="aptitude python3-dev gcc libc-dev libffi-dev firefox-esr chromium-driver" \
 && apt-get install -y --no-install-recommends --no-install-suggests $pythonDeps $build_dependencies \
 # Install chromedriver and chromium with aptitude
# && aptitude install chromium-driver -y \
 # Download and install geckodriver
 && curl -fL -o /tmp/geckodriver.tar.gz \
      https://github.com/mozilla/geckodriver/releases/download/v${geckodriver_ver}/geckodriver-v${geckodriver_ver}-linux64.tar.gz \
 && tar -xzf /tmp/geckodriver.tar.gz -C /tmp/ \
 && chmod +x /tmp/geckodriver \
 && mv /tmp/geckodriver /usr/bin/ \
 && python setup.py sdist bdist_wheel \
 && pip install -e . \
 && pip install pytest \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $build_dependencies \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*