#!/bin/bash

# install virtualenv
python3 -m pip install --user virtualenv

# create virtualenv
python3 -m virtualenv env

# TODO: exclude the env/ from your gitignore

 
# TODO: set something up for windows?
# deactivate virtualenv using: deactivate 
source env/bin/activate

# install packages from requirements
pip3 install -r requirements.txt

