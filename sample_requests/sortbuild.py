#!/bin/env python
import requests
import json

def have_a_build_num():
    BUILDS_URL='http://10.58.143.142:8888/api/build/builds/'
    response = requests.get(BUILDS_URL)
    builds = response.json()
    print builds
    last_num = sorted(builds['items'], key = lambda i: i['number'], reverse=True)[0]['number']
    number = int(last_num) + 1
    return number    

builds = have_a_build_num()
print builds
# print sorted(builds['items'], key = lambda i: i['number'], reverse=True)[0]['number']
