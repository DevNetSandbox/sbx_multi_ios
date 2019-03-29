mkdir jenkins_home
docker build -t myjenkins .
# probably should change these
echo "developer" | docker secret create jenkins-user -
echo "C1sco12345" | docker secret create jenkins-pass -

# run launch the stack
docker stack deploy -c docker-compose.yaml jenkins
