# update symlink to desired nso version
rm /opt/nso
ln -s /opt/nso47 /opt/nso
source /opt/nso47/ncsrc

# create virtualenv
virtualenv -p /usr/local/bin/python3.6 venv
source venv/bin/activate
pip install -r requirements.txt


#!/usr/bin/env bash
logfile=cicd-evpn-setup.log
gitlab_host="http://10.10.20.20"
gitlab_user="developer"
gitlab_password="C1sco12345"
repo_name="cicd-evpn"
gitlab_user="developer"

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

# installing telnet if not present
sudo yum install -y telnet

echo "Launching VIRL simulations (prod+test) ... "
root_dir=$(pwd)
cd $root_dir/virl/test
virl up --provision > /dev/null &
TEST=$!
cd $root_dir/virl/prod
virl up --provision &
PROD=$!
wait $TEST $PROD
cd $root_dir

echo "Launching NSO ... "
ncs-setup --dest .
ncs


echo "Importing Test network to NSO .. "
cd $root_dir/virl/test
virl generate nso 2>&1


# echo "Importing Prod network to NSO"
# cd $root_dir/virl/prod
# virl generate nso 2>&1

echo "Performing initial sync of devices..."
echo "devices sync-from" | ncs_cli -u admin -C

echo "Creating Repo on Gitlab"
cd $root_dir
create_gitlab_token 2>&1 >> $logfile
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=${repo_name}&visibility=public" "${gitlab_host}/api/v4/projects" 2>&1 >> $logfile

echo "Retrieve User Id for ${gitlab_user}"
user_id=$(curl -s -X GET --header "PRIVATE-TOKEN: $personal_access_token" "${gitlab_host}/api/v4/users?search=${gitlab_user}" | python -c "import sys, json; print(json.load(sys.stdin)[0]['id'])")
# echo "User Id for ${gitlab_user} is ${user_id}."

echo "Retrieve Project Id for ${repo_name}"
project_id=$(curl -s -X GET --header "PRIVATE-TOKEN: $personal_access_token" "${gitlab_host}/api/v4/projects?search=${repo_name}" | python -c "import sys, json; print(json.load(sys.stdin)[0]['id'])")
# echo "Project Id for ${repo_name} is ${project_id}."

echo "Create Project Labels for Issues"
doing_label_id=$(curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=Doing&color=#A8D695" "${gitlab_host}/api/v4/projects/${project_id}/labels" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=Bug&color=#FF0000" "${gitlab_host}/api/v4/projects/${project_id}/labels" 2>&1 >> $logfile
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=Enhancement&color=#0033CC" "${gitlab_host}/api/v4/projects/${project_id}/labels" 2>&1 >> $logfile
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=Research&color=#8E44AD" "${gitlab_host}/api/v4/projects/${project_id}/labels" 2>&1 >> $logfile
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=Change&color=#F0AD4E" "${gitlab_host}/api/v4/projects/${project_id}/labels" 2>&1 >> $logfile
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=ToProduction&color=#5CB85C" "${gitlab_host}/api/v4/projects/${project_id}/labels" 2>&1 >> $logfile
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=Urgent&color=#CC0033" "${gitlab_host}/api/v4/projects/${project_id}/labels" 2>&1 >> $logfile
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=Documentation&color=#428BCA" "${gitlab_host}/api/v4/projects/${project_id}/labels" 2>&1 >> $logfile
curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "name=Security&color=#D9534F" "${gitlab_host}/api/v4/projects/${project_id}/labels" 2>&1 >> $logfile

# ToDo: Enable the "Doing" list on the Project board
#   For some reason, the board isn't created until viewed via the Web GUI.  No API to create board documented
# echo "Create Board List for Doing"
# board_id=$(curl -s --header "PRIVATE-TOKEN: $personal_access_token" "${gitlab_host}/api/v4/projects/${project_id}/boards" | python -c "import sys, json; print(json.load(sys.stdin)[0]['id'])")
# curl -s --header "PRIVATE-TOKEN: $personal_access_token" -d "label_id=${doing_label_id}" "${gitlab_host}/api/v4/projects/${project_id}/boards/${board_id}/lists" 2>&1 >> $logfile

echo "Open Sample Issues for Demo"
./open_issues.py ${gitlab_host} ${personal_access_token} ${project_id} ${user_id} issues_list.csv 2>&1 >> $logfile

echo "Configure Git"
git config --global user.name "developer"
git config --global user.email "developer@devnetsandbox.cisco.com"

echo "Initalizing Local Repository"
git init
git remote add origin http://$gitlab_user:$gitlab_password@10.10.20.20/developer/${repo_name}.git

git add .
git checkout -b test
git commit -m "Initial commit"

echo "Pushing Branches"
git push -u origin test
git checkout -b production
git push -u origin production
git checkout test

echo "Test Network Summary"
cd $root_dir/virl/test
virl ls
virl nodes

echo "Production Network Summary"
cd $root_dir/virl/prod
virl ls
virl nodes
