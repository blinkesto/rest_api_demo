import logging

from flask import request
from flask_restplus import Resource
from rest_api_demo.api.build.business import create_server, update_server, delete_server
from rest_api_demo.api.build.serializers import server, page_of_servers
from rest_api_demo.api.build.parsers import pagination_arguments
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import Server

log = logging.getLogger(__name__)

ns = api.namespace('build/servers', description='Operations related to servers')


@ns.route('/')
class ServersCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_servers)
    def get(self):
        """
        Returns list of build posts.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        server_query = Server.query
        servers_page = server_query.paginate(page, per_page, error_out=False)

        return servers_page

    @api.expect(server)
    def post(self):
        """
        Creates a new server.
        """
        print(request.json)
        create_server(request.json)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Post not found.')
class ServerItem(Resource):

    @api.marshal_with(server)
    def get(self, id):
        """
        Returns a server
        """
        return Server.query.filter(Server.id == id).one()

    @api.expect(server)
    @api.response(204, 'Server successfully updated.')
    def put(self, id):
        """
        Updates a server
        """
        print('Update a server')
        data = request.json
        update_server(id, data)
        return None, 204

    @api.response(204, 'Server successfully deleted.')
    def delete(self, id):
        """
        Deletes build post.
        """
        delete_server(id)
        return None, 204


