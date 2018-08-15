#!/usr/bin/env bash
logfile=cicd-setup.log
gitlab_host="http://10.10.20.20"
gitlab_user="developer"
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

echo "Launching VIRL simulations (prod+test) ... "
root_dir=$(pwd)
cd $root_dir/virl/test
virl up --provision &
TEST=$!
cd $root_dir/virl/prod
virl up --provision &
PROD=$!
wait $TEST $PROD


echo "Launching NSO ... "
mkdir /home/cisco/nso-run
cd /home/cisco/ncs-run
ncs-setup --dest .
ncs


echo "Importing Test network to NSO .. "
cd $root_dir/virl/test
virl generate nso 2>&1


echo "Importing Prod network to NSO"
cd $root_dir/virl/prod
virl generate nso 2>&1

echo "Performing initial sync of devices..."
echo "devices sync-from" | ncs_cli -u admin -C

echo "Creating Repo on Gitlab"
cd $root_dir
create_gitlab_token 2>&1 >> $logfile
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=network-cicd&visibility=public" "http://10.10.20.20/api/v4/projects" 2>&1 >> $logfile


echo "Initalizing Local Repository"

git init
git remote add origin http://10.10.20.20/developer/network-cicd.git
git add .
git checkout -b test
git commit -m "Initial commit"
git push -u origin test
git checkout -b production
git push -u origin production
git checkout test
