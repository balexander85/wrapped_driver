FROM python:buster
ARG test_dependencies="chromium-driver"
ARG virtualenv_name="wrappeddriver-env"
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /app
COPY tests/requirements.txt ./
RUN apt-get update \
  && apt-get upgrade -y \
  # Install packages needed to build and test
  && apt-get install $test_dependencies -y \
  # Create Virtual Environment
  && python -m venv /$virtualenv_name \
  # Activate Virtual Environment
  && . /$virtualenv_name/bin/activate \
  && /$virtualenv_name/bin/python -m pip install --upgrade pip \
  && /$virtualenv_name/bin/python -m pip install -r requirements.txt \
  # Cleanup unnecessary stuff
  && apt-get purge -y --auto-remove \
                   -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
            /tmp/*
