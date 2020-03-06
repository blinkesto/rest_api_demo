import logging

from flask import request
from flask_restx import Resource, fields
from rest_api_demo.api.build.serializers import csv, page_of_csvs, server, page_of_servers
from rest_api_demo.api.build.parsers import pagination_arguments
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import Csv, Server
from rest_api_demo.api.util import utils
from rest_api_demo.api.build.business import create_server
import json

log = logging.getLogger(__name__)

ns = api.namespace('qc/load_servers', description='Populate servers table with minion_map')

minion_def = api.model('minion_def', {
    'host': fields.String(''),
    'os': fields.String(''),
    'fqdn': fields.String(''),
})
minion_map = api.model('minion_map', {
    'data': fields.Nested(server),
    })
@ns.route('/')
@api.response(404, 'Post not found.')
class Parse(Resource):
    @api.expect(page_of_servers)
    def post(self, ):
        servers = request.json

        for server in servers['items']:
            create_server(server)
                 
        
        return None, 201

    @api.expect(minion_map)
    def put(self, ):
        request_json = request.json
        # minion_map["data"] = # {{"usmdclxn00259.nix.us.kworld.kpmg.com": {"host": "usmdclxn00259", "os": "redhat", "fqdn": "usmdclxn00259.nix.us.kworld.kpmg.com"}, "USMDCKNCL70076": {"host": "usmdckncl70076", "os": "windows", "fqdn": "usmdckncl70076.us.kworld.kpmg.com"}, "USMDCKNCL70077": {"host": "usmdckncl70077", "os": "windows", "fqdn": "usmdckncl70077.us.kworld.kpmg.com"}, "USMDCKNCL70078": {"host": "usmdckncl70078", "os": "windows", "fqdn": "usmdckncl70078.us.kworld.kpmg.com"}}
        
        for id, minion in request_json.iteritems():
            # server = Server(minion["host"], "init", "", "", minion['os'], minion['fqdn'])
            create_server(minion)
            print(minion)
        return request_json
