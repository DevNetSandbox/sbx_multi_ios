FROM debian:stable-slim
RUN apt-get update && apt-get install -y curl

ADD pipeline /pipeline

ADD ./parser.conf /parser.conf
ADD ./config /etc/pipeline
#ADD ./data /data
ADD ./startup.sh ./startup.sh
VOLUME ["/etc/pipeline"]
WORKDIR /
CMD ./startup.sh
