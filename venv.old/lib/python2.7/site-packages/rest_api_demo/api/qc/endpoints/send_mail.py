import logging

from flask import request
from flask_restplus import Resource, fields
from rest_api_demo.api.qc.business import send_mail
from rest_api_demo.api.build.serializers import csv, page_of_csvs
from rest_api_demo.api.build.parsers import pagination_arguments
from rest_api_demo.api.restplus import api
from rest_api_demo.database.models import Csv
from rest_api_demo.api.util import utils
log = logging.getLogger(__name__)

ns = api.namespace('qc/send_mail', description='Send an email')

mail_message = api.model('mail_message', {
    'to': fields.String('To email'), 
    'from_email': fields.String('From email'),
    'subject': fields.String('Subject'),
    'text': fields.String('Body Text'),
    'html': fields.String('Body HTML'),
    'files': fields.String('Files to attach'),
    'server': fields.String('smtpout.us.kworld.kpmg.com'),
    })

@ns.route('/')
@api.response(404, 'Post not found.')
class Parse(Resource):
    @api.expect(mail_message)
    def post(self, ):
        data = request.json
        
        ret_data = send_mail(data)        

        return ret_data