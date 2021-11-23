FROM balexander85/wrapped_driver:slim-buster
ARG geckodriver_ver=0.30.0
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
   https://github.com/mozilla/geckodriver/archive/refs/tags/v${geckodriver_ver}.tar.gz \
 && tar -xzf /tmp/geckodriver.tar.gz -C /tmp/ \
 && curl https://sh.rustup.rs -sSf | sh -s -- -y \
 && . $HOME/.cargo/env \
 && rustup target install armv7-unknown-linux-gnueabihf \
 && cat /usr/src/arm_config >> /tmp/geckodriver-${geckodriver_ver}/.cargo/config \
 && cd /tmp/geckodriver-${geckodriver_ver} \
 && cargo build --release --target armv7-unknown-linux-gnueabihf \
 && mv /tmp/geckodriver-0.30.0/target/armv7-unknown-linux-gnueabihf/release/geckodriver /usr/bin/geckodriver \
 && . /wrapped-driver-env/bin/activate \
 && pip install pytest \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $build_dependencies \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*
