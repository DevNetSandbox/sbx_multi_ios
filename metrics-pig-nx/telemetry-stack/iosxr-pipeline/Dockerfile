FROM debian:stable-slim

RUN apt-get update && apt-get install -y curl
# Stage default configuration, metrics spec and example setup
ADD pipeline /pipeline
ADD ./parser.conf /parser.conf
ADD ./config /etc/pipeline
ADD ./startup.sh ./startup.sh

VOLUME ["/data"]
WORKDIR /

EXPOSE 5432
CMD ./startup.sh &
