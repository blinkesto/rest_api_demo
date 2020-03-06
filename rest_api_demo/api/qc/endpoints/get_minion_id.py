import logging

from flask import request
from flask_restx import Resource, fields
from rest_api_demo.api.qc.business import get_minion_id
from rest_api_demo.api.build.serializers import csv, page_of_csvs
from rest_api_demo.api.build.parsers import pagination_arguments
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import Csv
from rest_api_demo.api.util import utils
log = logging.getLogger(__name__)

ns = api.namespace('qc/get_minion_id', description='Find the Salt Minion ID of a host')

host_query = api.model('host_query', {
    'list': fields.List(fields.String), 
    })

@ns.route('/')
@api.response(404, 'Post not found.')
class Parse(Resource):
    @api.expect(host_query)
    def post(self, ):
        data = request.json
        
        ret_data = get_minion_id(data)        
        print("Got: {0}".format(ret_data))
        return ret_data
