import logging.config

import os
from flask import Flask, Blueprint
from rest_api_demo import settings
from rest_api_demo.api.build.endpoints.servers import ns as server_namespace
from rest_api_demo.api.build.endpoints.builds import ns as build_namespace
from rest_api_demo.api.build.endpoints.server_histories import ns as server_history_namespace
from rest_api_demo.api.build.endpoints.csvs import ns as csv_namespace
from rest_api_demo.api.build.endpoints.parse import ns as parse_namespace
from rest_api_demo.api.qc.endpoints.send_mail import ns as send_mail
from rest_api_demo.api.qc.endpoints.load_servers import ns as load_servers
from rest_api_demo.api.qc.endpoints.get_minion_id import ns as get_minion_id
from rest_api_demo.api.restplus import api
from rest_api_demo.database import db


app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app, ):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(server_namespace)
    api.add_namespace(build_namespace)
    api.add_namespace(server_history_namespace)
    api.add_namespace(csv_namespace)
    api.add_namespace(parse_namespace)
    api.add_namespace(send_mail)
    api.add_namespace(load_servers)    
    api.add_namespace(get_minion_id)
    
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
