#!/usr/bin/env bash

gitlab_host="http://10.10.20.50"
gitlab_user="root"
gitlab_password="C1sco12345"

# create gitlab personal access token
# https://gist.github.com/michaellihs/5ef5e8dbf48e63e2172a573f7b32c638
create_gitlab_token () {
  # curl for the login page to get a session cookie and the sources with the auth tokens
  body_header=$(curl -c /tmp/cookies.txt -i "${gitlab_host}/users/sign_in" -s)
  # grep the auth token for the user login for
  #   not sure whether another token on the page will work, too - there are 3 of them
  csrf_token=$(echo $body_header | perl -ne 'print "$1\n" if /new_user.*?authenticity_token"[[:blank:]]value="(.+?)"/' | sed -n 1p)
  # send login credentials with curl, using cookies and token from previous request
  curl --silent -b /tmp/cookies.txt -c /tmp/cookies.txt -i "${gitlab_host}/users/sign_in" \
      --data "user[login]=${gitlab_user}&user[password]=${gitlab_password}" \
      --data-urlencode "authenticity_token=${csrf_token}"

  # send curl GET request to personal access token page to get auth token
  body_header=$(curl --silent -H 'user-agent: curl' -b /tmp/cookies.txt -i "${gitlab_host}/profile/personal_access_tokens" -s)
  csrf_token=$(echo $body_header | perl -ne 'print "$1\n" if /authenticity_token"[[:blank:]]value="(.+?)"/' | sed -n 1p)

  # curl POST request to send the "generate personal access token form"
  # the response will be a redirect, so we have to follow using `-L`
  body_header=$(curl --silent -L -b /tmp/cookies.txt "${gitlab_host}/profile/personal_access_tokens" \
      --data-urlencode "authenticity_token=${csrf_token}" \
      --data 'personal_access_token[name]=golab-generated&personal_access_token[expires_at]=&personal_access_token[scopes][]=api')

  personal_access_token=$(echo $body_header | perl -ne 'print "$1\n" if /created-personal-access-token"[[:blank:]]value="(.+?)"/' | sed -n 1p)

}

# prints colored text
success () {
    COLOR="92m"; # green
    STARTCOLOR="\e[$COLOR";
    ENDCOLOR="\e[0m";
    printf "$STARTCOLOR%b$ENDCOLOR" "done\n";
}

# FirewallD stopped in sandbox image
# echo ""
# echo "Ensuring firewalld is stopped and disabled"
# sudo systemctl stop firewalld
# sudo systemctl disable firewalld
# sudo systemctl restart docker

echo ""
printf "Launching Gitlab CE ..."
docker-compose up -d 2> gitlab_setup.log
success

printf "Waiting for Gitlab CE to become available ."

until $(curl --output /dev/null --silent --head --fail http://10.10.20.50); do
    printf '.'
    sleep 10
done
success

printf "Configuring external URL for GitLab"
docker-compose exec gitlab /bin/bash -c "echo external_url \'http://10.10.20.50\' >> /etc/gitlab/gitlab.rb"
docker-compose exec gitlab gitlab-ctl reconfigure 2>&1 >> gitlab_setup.log

printf "Registering GitLab Runner ... "

docker-compose exec runner1 gitlab-runner register 2>&1 >> gitlab_setup.log
success
printf "Creating user 'developer' ..."
create_gitlab_token 2>&1 >> gitlab_setup.log
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "email=developer@devnetsandbox.cisco.com&password=C1sco12345&username=developer&name=developer&skip_confirmation=true" "http://10.10.20.50/api/v4/users" 2>&1 >> gitlab_setup.log
success

echo "Updating git global config on devbox"
git config --global user.name "Developer"
git config --global user.email developer@devnetsandbox.cisco.com
