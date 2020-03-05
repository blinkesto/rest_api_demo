import logging

from flask import request
from flask_restplus import Resource
from rest_api_demo.api.build.business import create_csv, update_csv, delete_csv
from rest_api_demo.api.build.serializers import csv, page_of_csvs
from rest_api_demo.api.build.parsers import pagination_arguments
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import Csv

log = logging.getLogger(__name__)

ns = api.namespace('build/Csvs', description='Operations related to server csv')


@ns.route('/')
class CsvsCollection(Resource):    
    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_csvs)
    def get(self):
        """
        Returns list of build posts.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        csv_query = Csv.query
        csvs_page = csv_query.paginate(page, per_page, error_out=False)

        return csvs_page

    @api.expect(csv)
    def post(self):
        """
        Creates a new server history.
        """
        print(request.json)
        create_csv(request.json)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Post not found.')
class CSVItem(Resource):

    @api.marshal_with(csv)
    def get(self, id):
        """
        Returns a server
        """
        return Csv.query.filter(Csv.id == id).one()

    @api.expect(csv)
    @api.response(204, 'Csv successfully updated.')
    def put(self, id):
        """
        Updates a csv
        """
        print('Update a csv')
        data = request.json
        update_csv(id, data)
        return None, 204

    @api.response(204, 'Csv successfully deleted.')
    def delete(self, id):
        """
        Deletes build post.
        """
        delete_csv(id)
        return None, 204

