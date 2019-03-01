# install required packages
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# clone needed repositories
git clone https://github.com/ansible/awx.git awx-repo

# copy our files in
cp inventory awx/installer/inventory
#

cd awx-repo

git clone https://github.com/ansible/awx-logos.git
cd installer/
ansible-playbook -i inventory install.yml -vv
