# NON PERSISTEND METHODS 

api/build/endpoint/new_endpoint.py
~~~python
    ...
    from flask_restplus import Resource, fields
    ...

    ns = api.namespace('send_mail', description='Send an email')

    mail_message = api.model('mail_message', {'to': fields.String('To email'), 'from_email': fields.String('From email')})

    @ns.route('/')
    @api.response(404, 'Post not found.')
    class SendMail(Resource):
        @api.expect(mail_message)
        def post(self, ):
            data = request.json
            
            ret_data = send_mail(data)        

            return ret_data
~~~
api/build/business.py
~~~python
    def send_mail(data):
        to = data.get('to')
        from_email = data.get('from_email')

        return { 'to': to, 'from_email': from_email }
~~~


# PERSISTENT METHODS 

Add a row to existing

Create a new table "Object"
Add class in database/models.py

- api/build/business.py
    from rest_api_demo.database.models import Server, Build, ServerHistory, <Object>
    ...
    def create_<Object>(data):

    def update_<Object>():

    def delete_<Object>():

- api/build/serializers.py

- api/build/endpoints/<Object>.py

- flaskr.py
    from rest_api_demo.api.build.endpoints.<Object> import ns as <Object>_namespace
    def initialize_app(flask_app, ):
        ...
        api.add_namespace(<Object>_namespace)
        ...

jump
rsync -avz ~/projects/rest_api_demo/ prahtdooley@10.58.143.142:/home/prahtdooley/projects/rest_api_demo

master
rm dist/rest_api_demo-1.0.0* && python setup.py sdist bdist_wheel && pip uninstall -y rest-api-demo && pip install dist/rest_api_demo-1.0.0.tar.gz 


v2