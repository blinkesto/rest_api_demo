#!/bin/env python
#  ./update_server.py 1 mystatus2
import requests
import json
import sys

server_id=sys.argv[1]
name=sys.argv[2]
status=sys.argv[3]
build_id=sys.argv[4]

_URL='http://localhost:8888/api/blog/servers/%s' % server_id
#_data={'name':'%s' % name, 'status':'%s' % status, 'build_id': build_id}
_data={"name":"%s" % name, "status":"%s" % status, "build_id": build_id}
print(_data)
print(_URL)
x = requests.put(_URL, json=_data)
print(x.status_code)

_URL='http://localhost:8888/api/blog/servers/%s' % server_id

x = requests.get(_URL)
print(x.text)
