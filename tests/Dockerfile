# instructions for building geckodriver for ARM
# https://firefox-source-docs.mozilla.org/testing/geckodriver/ARM.html
FROM python:slim-buster as gecko-image
ARG geckodriver_ver=0.30.0
ARG build_dependencies="curl gcc-arm-linux-gnueabihf libc6-armhf-cross libc6-dev-armhf-cross"
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
COPY arm_config .
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends --no-install-suggests $build_dependencies \
 # Download and install dependencies needed for geckodriver
 && curl -fL -o /tmp/geckodriver.tar.gz \
    https://github.com/mozilla/geckodriver/archive/refs/tags/v${geckodriver_ver}.tar.gz \
 && tar -xzf /tmp/geckodriver.tar.gz -C / \
 && curl https://sh.rustup.rs -sSf | sh -s -- -y \
 && . $HOME/.cargo/env \
 && rustup target install armv7-unknown-linux-gnueabihf \
 && cat arm_config >> /geckodriver-${geckodriver_ver}/.cargo/config \
 && cd /geckodriver-${geckodriver_ver} \
 && cargo build --release --target armv7-unknown-linux-gnueabihf \
 && mv /geckodriver-${geckodriver_ver}/target/armv7-unknown-linux-gnueabihf/release/geckodriver /geckodriver

FROM balexander85/wrapped_driver:latest
ARG test_dependencies="firefox-esr chromium-driver"
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY base_test.py \
     conftest.py \
     pytest.ini \
     test_wrapped_driver.py \
     test_wrapped_driver_integration.py ./
COPY --from=gecko-image /geckodriver /usr/bin/geckodriver
RUN apt-get update \
 && apt-get upgrade -y \
 # Install tools for building and testing
 && apt-get install -y --no-install-recommends --no-install-suggests $test_dependencies \
 && . /wrapped-driver-env/bin/activate \
 && pip install pytest \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $build_dependencies \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*

