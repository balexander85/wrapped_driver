FROM balexander85/wrapped_driver:slim-buster
ARG geckodriver_ver=0.23.0
ARG build_dependencies="curl bzip2 gcc-arm-linux-gnueabihf libc6-armhf-cross libc6-dev-armhf-cross"
ARG test_dependencies="firefox-esr chromium-driver"
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY . .
RUN apt-get update \
 && apt-get upgrade -y \
 # Install tools for building and testing
 && apt-get install -y --no-install-recommends --no-install-suggests $test_dependencies $build_dependencies \
 # Download and install dependencies needed for geckodriver
 && curl -fL -o /tmp/geckodriver.tar.gz \
      https://github.com/mozilla/geckodriver/releases/download/v${geckodriver_ver}/geckodriver-v${geckodriver_ver}-arm7hf.tar.gz \
 && tar -xzf /tmp/geckodriver.tar.gz -C /tmp/ \
 && chmod +x /tmp/geckodriver \
 && mv /tmp/geckodriver /usr/bin/ \
 && . /wrapped-driver-env/bin/activate \
 && pip install pytest \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $build_dependencies \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*