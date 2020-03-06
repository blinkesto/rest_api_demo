# Flask settings
# 10.58.143.137
# FLASK_SERVER_NAME = '172.31.47.65:8888'
# FLASK_SERVER_NAME = 'ec2-18-188-136-183.us-east-2.compute.amazonaws.com:8888'
# FLASK_SERVER_NAME = 'ec2-3-18-92-220.us-east-2.compute.amazonaws.com:8888'
FLASK_SERVER_NAME = 'localhost:8888'

FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = True

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
