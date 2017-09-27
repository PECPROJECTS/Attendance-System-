#!/bin/bash/

virtualenv rest-api
source rest-api/bin/activate

pip install flask
pip install flask-restful
pip install sqlalchemy
