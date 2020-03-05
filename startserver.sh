#!/bin/sh

python rest_api_demo/flaskr.py 2>&1 |tee -a debug.out
