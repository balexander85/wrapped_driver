FROM python:3.7-slim-buster
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY tests \
  wrapped_driver/src \
  wrapped_driver/requirements.txt ./
RUN apt-get update \
 && apt-get upgrade -y \
 # Install tools for building
 && toolDeps="git aptitude" \
 && apt-get install -y --no-install-recommends --no-install-suggests $toolDeps \
 # Install chromedriver and chromium with aptitude
 && aptitude install chromium-driver -y \
 && pip install -r requirements.txt \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $toolDeps \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*
CMD ["python", "-m", "pytest", "-vv", "wrapped_driver/tests/"]

