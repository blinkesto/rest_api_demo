from rest_api_demo.database import db
# Import model from database/models.py
from rest_api_demo.database.models import Server, Build, ServerHistory, Csv
from sqlalchemy.exc import *
from werkzeug.exceptions import BadRequest
import csv
import io

# CREATE CRUD METHODS
def create_server(data):
    minion_id = data.get('minion_id')
    server_id = data.get('id')
    status = data.get('status')
    build_id = data.get('build_id')
    ip = data.get('ip')
    servercsv = data.get('csv')
    histories = data.get('histories')
    os = data.get('os')
    fqdn = data.get('fqdn')

    # if servercsv:
    #     create_csv(servercsv)

    # if server_id:
    #     server.id = server_id

    server = Server(minion_id, status, build_id, ip, os, fqdn)
    test = db.session.add(server)
    db.session.commit()

    for history in histories:
        new_history = ServerHistory(server.id, history['log'])
        db.session.add(new_history)

    db.session.commit()        

def update_server(server_id, data):
    print('Update Server')
    server = Server.query.filter(Server.id == server_id).one()
    server.minion_id = data.get('minion_id')
    server.status = data.get('status')
    server.ip = data.get('ip')
    servercsv = data.get('servercsv')
    os = data.get('os')
    fqdn = data.get('fqdn')

    if data.get('build_id') is not None:
        server.build_id = data.get('build_id')

    db.session.add(server)
    db.session.commit()


def delete_server(server_id):
    server = Server.query.filter(Server.id == server_id).one()
    server_histories = ServerHistory.query.filter(Server.id == server_id)
    for server_history in server_histories:
        db.session.delete(server_history)
    db.session.delete(server)
    db.session.commit()


# BUILD 
def create_build(data):
    build_id = data.get('id')
    number = data.get('number')
    servers = Server.query.filter(Server.build_id == build_id)
    build = Build(number, servers)

    if build_id:
        build.id = build_id

    db.session.add(build)
    try:
        db.session.commit()
    except IntegrityError as ie:
        print("IntegrityError: %s.  Build number: %s" % (ie.message, number))
        raise BadRequest("IntegrityError: %s.  Build number: %s" % (ie.message, number))


def update_build(build_id, data):
    build = Build.query.filter(Build.id == build_id).one()
    build.number = data.get('number')
    db.session.add(build)
    db.session.commit()


def delete_build(build_id):
    build = Build.query.filter(Build.id == build_id).one()
    db.session.delete(build)
    db.session.commit()


# SERVER HISTORY 
def create_server_history(data):
    server_history_id = data.get('id')
    server_id = data.get('server_id')
    log = data.get('log')
    timestamp = data.get('timestamp')

    server_history = ServerHistory(server_id, log)

    if server_history_id:
        server_history.id = server_history_id

    db.session.add(server_history)
    db.session.commit()


def update_server_history(server_history_id, data):
    server_history = ServerHistory.query.filter(ServerHistory.id == server_history_id).one()
    server_history.server_id = data.get('server_id')
    server_history.log = data.get('log')
    server_history.timestamp = data.get('timestamp')
	
    db.session.add(build)
    db.session.commit()


def delete_server_history(server_history_id):
    server_history = ServerHistory.query.filter(ServerHistory.id == server_history_id).one()
    db.session.delete(server_history)
    db.session.commit()


# SERVER CSV
def create_csv(data):
    csv_id = data.get('id')
    server_id = data.get('server_id')
    demand_number = data.get('demand_number')
    hostname = data.get('hostname')
    csv_data = data.get('csv_data')

    csv = Csv(server_id, demand_number, hostname, csv_data)

    if csv_id:
        csv.id = csv_id

    db.session.add(csv)
    db.session.commit()

def update_csv(csv_id, data):
    csv = ServerCSV.query.filter(Csv.id == csv_id).one()
    csv.server_id = data.get('server_id')
    csv.demand_number = data.get('demand_number')
    csv.hostname = data.get('hostname')
    csv_data = data.get('csv_data')
	
    db.session.add(build)
    db.session.commit()

def delete_csv(csv_id):
    csv = Csv.query.filter(Csv.id == csv_id).one()
    db.session.delete(csv)
    db.session.commit()

def parse_csv(csv_id, data):
    csv_path = data.get('csv_path')
	
    try:
        config = csv.DictReader(io.open(csv_path, 'r'))
        print("OPened")
    except Exception, e:
        str(e)
        
    return csv_path

def send_mail(data):
    to = data.get('to')
    from_email = data.get('from_email')

    return { 'to': to, 'from_email': from_email }