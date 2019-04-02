# Using pyATS with Jenkins

## Setup


1. Add Gitlab Server to your devbox. See instructions [here](./gitlab)

2. Add Jenkins to your devbox. See instructions [here](./jenkins)


3. Initialize a pyats project

```

# generate new project from cookiecutter
cookiecutter gh:kecorbin/cookiecutter-pyats

# create virtualenv and install deps
cd <generated directory>
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# launch a sim
virl pull virlfiles/xe-xr-nx
virl up --provision
virl generate pyats -o testbeds/default.yaml

# run validations against simulation
./run.sh
```

3. Create Repo on Gitlab Server
    * http://10.10.20.20/
    * New -> Project
