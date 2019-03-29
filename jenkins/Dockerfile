FROM jenkins/jenkins:lts
# if we want to install via apt
USER root
RUN apt-get update && apt-get install -y ruby make wget
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
