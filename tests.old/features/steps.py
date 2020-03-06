from lettuce import *
import requests
import json
from rest_api_demo.flaskr import app
from rest_api_demo.api.build.business import *
# from rest_api_demo.database.models import Server
# from rest_api_demo.api.build import business 

@before.all
def before_all():
    
    world.test_client = app.test_client()
    data={
        "build_id": "1234",
        "ip": "1.1.1.1",
        "name": "server1",
        "status": "Init"
    }
    create_server(data)


# @step('I have a build')
# def have_a_build_num(step):
#     BUILDS_URL='http://10.58.143.142:8888/api/build/builds/'
#     response = requests.get(BUILDS_URL)
#     builds = response.json()
#     last_num = sorted(builds['items'], key = lambda i: i['number'], reverse=True)[0]['number']
#     number = int(last_num) + 1
#     world.number = str(number)

# @step('I add the build')
# def call(step):
#     BUILDS_URL='http://10.58.143.142:8888/api/build/builds/'
#     build_data={'number':world.number, 'servers':[]}
    
#     response = requests.post(BUILDS_URL, json=build_data)
#     world.status_code = response.status_code 

# @step('I see the response (\d+)')
# def check_response(step, expected):
#     assert world.status_code == int(expected), \
#         "Got %d" % world.status_code
