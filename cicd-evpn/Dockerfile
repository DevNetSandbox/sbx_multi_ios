FROM ciscotestautomation/pyats:latest-robot
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD . /cicd-evpn
WORKDIR /cicd-evpn
ENTRYPOINT bash /cicd-evpn/docker-entrypoint.sh
