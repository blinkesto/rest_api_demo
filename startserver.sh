#!/bin/sh

# rm dist/rest_api_demo-1.0.0* && python setup.py sdist bdist_wheel && pip uninstall -y rest-api-demo && pip install dist/rest_api_demo-1.0.0.tar.gz && python reset_db.py
export PYTHONPATH=`pwd`
export FLASK_SERVER_NAME='ec2-3-18-92-220.us-east-2.compute.amazonaws.com:8888'
python rest_api_demo/flaskr.py 2>&1 |tee -a debug.out
