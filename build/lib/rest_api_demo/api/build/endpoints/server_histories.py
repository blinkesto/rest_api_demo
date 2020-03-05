import logging

from flask import request
from flask_restplus import Resource
from rest_api_demo.api.build.business import create_server_history, update_server_history, delete_server_history
from rest_api_demo.api.build.serializers import server_history, page_of_server_histories
from rest_api_demo.api.build.parsers import pagination_arguments
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import ServerHistory

log = logging.getLogger(__name__)

ns = api.namespace('build/serverhistories', description='Operations related to server histories')


@ns.route('/')
class ServerHistoriesCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_server_histories)
    def get(self):
        """
        Returns list of build posts.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        server_history_query = ServerHistory.query
        server_histories_page = server_history_query.paginate(page, per_page, error_out=False)

        return server_histories_page

    @api.expect(server_history)
    def post(self):
        """
        Creates a new server history.
        """
        print(request.json)
        create_server_history(request.json)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Post not found.')
class ServerHistoryItem(Resource):

    @api.marshal_with(server_history)
    def get(self, id):
        """
        Returns a server
        """
        return ServerHistory.query.filter(ServerHistory.id == id).one()

    @api.expect(server_history)
    @api.response(204, 'ServerHistory successfully updated.')
    def put(self, id):
        """
        Updates a server
        """
        print('Update a server history')
        data = request.json
        update_server_history(id, data)
        return None, 204

    @api.response(204, 'Server successfully deleted.')
    def delete(self, id):
        """
        Deletes build post.
        """
        delete_server_history(id)
        return None, 204


