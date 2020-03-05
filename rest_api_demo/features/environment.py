# https://behave.readthedocs.io/en/latest/usecase_flask.html
import os
import tempfile
from behave import fixture, use_fixture
from flaskr import app, initialize_app


@fixture
def flaskr_client(context, *args, **kwargs):
    context.db, app.config['DATABASE'] = tempfile.mkstemp()
    app.testing = True

    context.client = app.test_client()
    with app.app_context():
        initialize_app(app) 
    yield context.client


def before_feature(context, feature):
    use_fixture(flaskr_client, context)
