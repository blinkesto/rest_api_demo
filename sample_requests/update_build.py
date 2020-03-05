#!/bin/env python
#  ./update_server.py <build_id> <name>
# Cannot change servers here to change servers update the build_id for the server
import requests
import json
import sys

_id=sys.argv[1]
number=sys.argv[2]

_URL='http://localhost:8888/api/blog/builds/%s' % _id
_data={"number": number}
print(_data)
print(_URL)
x = requests.put(_URL, json=_data)
print(x.status_code)

_URL='http://localhost:8888/api/blog/builds/%s' % _id

x = requests.get(_URL)
print(x.text)
