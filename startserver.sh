#!/bin/sh

# rm dist/rest_api_demo-1.0.0* && python setup.py sdist bdist_wheel && pip uninstall -y rest-api-demo && pip install dist/rest_api_demo-1.0.0.tar.gz && python reset_db.py
export PYTHONPATH=`pwd`
python rest_api_demo/flaskr.py 2>&1 |tee -a debug.out
