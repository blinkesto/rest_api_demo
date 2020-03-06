import logging

from flask import request
from flask_restx import Resource
from rest_api_demo.api.build.business import create_csv, update_csv, delete_csv, parse_csv
from rest_api_demo.api.build.serializers import csv, page_of_csvs
from rest_api_demo.api.build.parsers import pagination_arguments
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import Csv

log = logging.getLogger(__name__)

ns = api.namespace('build/Parse', description='Operations related to parsing csv')


@ns.route('/<int:id>')
@api.response(404, 'Post not found.')
class Parse(Resource):
    @api.expect(csv)
    @api.response(204, 'Csv successfully updated.')
    def post(self, id):
        data = request.json
        csv_path = parse_csv(id, data)

        return { "csv_path": csv_path }