FROM python:3.7-slim-buster
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY wrapped_driver ./
RUN apt-get update \
 && apt-get upgrade -y \
 # Install tools for building
 && toolDeps="git aptitude" \
 && pythonDeps="python3-dev gcc libc-dev libffi-dev" \
 && apt-get install -y --no-install-recommends --no-install-suggests $pythonDeps $toolDeps \
 # Install chromedriver and chromium with aptitude
 && aptitude install chromium-driver -y \
 && pip install -r requirements.txt \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $toolDeps \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*