from flask_restx import fields
from rest_api_demo.api.restplus import api


pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})


csv = api.model('Csv', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a Csv'),
    'server_id': fields.String(attribute='server.id'),
    'demand_number': fields.String(required=True, description='Demand Number'),
    'hostname': fields.String(required=True, description='Hostname'),
    'csv_path': fields.String(required=True, description='Path to CSV'),
})

page_of_csvs = api.inherit('Page of server csvs', pagination, {
    'items': fields.List(fields.Nested(csv))
})

server_history = api.model('ServerHistory', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a ServerHistory'),
    'server_id': fields.String(attribute='server.id'),
    'log': fields.String(required=True, description='Log message'),
    'timestamp': fields.DateTime(),
})

page_of_server_histories = api.inherit('Page of server histories', pagination, {
    'items': fields.List(fields.Nested(server_history))
})


#
server = api.model('Server', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a Server'),
    'minion_id': fields.String(required=True, description='Minion ID'),
    'status': fields.String(required=True, description='Server Status'),
    'build_id': fields.String(attribute='build.id'),
    'ip': fields.String(required=False, description='Server IP'),
    # 'csv': fields.Nested(csv, required=False),
    'histories': fields.List(fields.Nested(server_history)),
    'os': fields.String(required=False, description='OS'),
    'fqdn': fields.String(required=True, description='fqdn'),
})

page_of_servers = api.inherit('Page of servers', pagination, {
    'items': fields.List(fields.Nested(server))
})

#
build = api.model('Build', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a Build'),
    'number': fields.String(required=True, description='Build number'),
    'servers': fields.List(fields.Nested(server))
})

page_of_builds = api.inherit('Page of builds', pagination, {
    'items': fields.List(fields.Nested(build))
})




