FROM jenkins/jenkins:lts
# if we want to install via apt
USER root
RUN apt-get update && \
    apt-get install -qqy ruby make wget python3-dev python3-venv \
            apt-transport-https ca-certificates curl gnupg2 \
            software-properties-common
# Install Docker from official repo
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    apt-key fingerprint 0EBFCD88 && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update -qq && \
    apt-get install -qqy docker-ce && \
    usermod -aG docker jenkins && \
    chown -R jenkins:jenkins $JENKINS_HOME/
# drop back to the regular jenkins user - good practice
USER jenkins
# disable setup wizard and prepopulate auth config
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
COPY security.groovy /usr/share/jenkins/ref/init.groovy.d/security.groovy
# install common plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt
# copy downloaded plugins
COPY plugins/*.hpi /usr/share/jenkins/ref/plugins/
USER root
# install pyATS
RUN python3 -m venv /pyats
RUN /pyats/bin/pip install genie
