mkdir jenkins_home
docker build -t jenkins .
docker run -v /var/run/docker.sock:/var/run/docker.sock \
           -v $(pwd)/jenkins_home:/var/jenkins_home \
           -p 8000:8080 \
           -p 50000:50000 \
           -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false" \
           jenkins
