#!/bin/env python

import requests
import json

_URL='http://localhost:8888/api/blog/servers/'

x = requests.get(_URL)
print(x.text)
