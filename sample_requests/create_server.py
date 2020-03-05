#!/bin/env python

import requests
import json
import sys

name=sys.argv[1]
status='Init'
build_id=sys.argv[2]

_URL='http://10.58.143.142:8888/api/build/servers/'
_data={'name':name, 'status':status, 'build_id':build_id}

x = requests.post(_URL, json=_data)
print(x.status_code)

x = requests.get(_URL)
print(x.text)
