import logging

from flask import request
from flask_restx import Resource
from rest_api_demo.api.build.business import create_build, update_build, delete_build
from rest_api_demo.api.build.serializers import build, page_of_builds
from rest_api_demo.api.build.parsers import pagination_arguments
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import Build

log = logging.getLogger(__name__)

ns = api.namespace('build/builds', description='Operations related to Jenkins builds ')


@ns.route('/')
class BuildsCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_builds)
    def get(self):
        """
        Returns list of build posts.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        build_query = Build.query
        builds_page = build_query.paginate(page, per_page, error_out=False)

        return builds_page

    @api.expect(build)
    def post(self):
        """
        Creates a new build.
        """
        create_build(request.json)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Build not found.')
class BuildItem(Resource):

    @api.marshal_with(build)
    def get(self, id):
        """
        Returns a build
        """
        return Build.query.filter(Build.id == id).one()

    @api.expect(build)
    @api.response(204, 'Build successfully updated.')
    def put(self, id):
        """
        Updates a build
        """
        data = request.json
        update_build(id, data)
        return None, 204

    @api.response(204, 'Build successfully deleted.')
    def delete(self, id):
        """
        Deletes build 
        """
        delete_build(id)
        return None, 204


