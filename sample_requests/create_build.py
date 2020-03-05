#!/bin/env python

import requests
import json
import sys

build_num=sys.argv[1]

BUILDS_URL='http://localhost:8888/api/blog/builds/'
build_data={'number':build_num, 'servers':[]}

x = requests.post(BUILDS_URL, json=build_data)
print(x.status_code)

x = requests.get(BUILDS_URL)
print(x.text)
