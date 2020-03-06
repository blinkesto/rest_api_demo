# https://docs.sqlalchemy.org/en/13/orm/relationships.html#one-to-one

from datetime import datetime
from rest_api_demo.database import db
from sqlalchemy.orm import relationship
from flask_restx import fields


class Server(db.Model):
    __tablename__ = 'server'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    minion_id = db.Column(db.String(255))
    status = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(50))
    os = db.Column(db.String(50))
    fqdn = db.Column(db.String(255))


    build_id = db.Column(db.Integer, db.ForeignKey('build.id'), nullable=False)    
    histories = db.relationship('ServerHistory', backref='server')
    # backref is tablename
    # csv = db.relationship("Csv", uselist=False, backref="server")

    def __init__(self, minion_id, status, build_id, ip, os, fqdn):
        self.minion_id = minion_id
        self.status = status
        self.build_id = build_id
        self.ip = ip
        self.os = os
        self.fqdn = fqdn
        # self.histories = histories
        # self.csv = csv

    def __repr__(self):
        return '<Server %r>' % self.minion_id


class Build(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(50), unique=True)
    servers = db.relationship('Server', backref='build', lazy='dynamic')

    def __init__(self, number, servers):
        self.number = number
        self.servers = servers

    def __repr__(self):
        return '<Build %r>' % self.number


class ServerHistory(db.Model):
    __tablename__ = 'serverhistory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)

    def __init__(self, server_id, log):
        self.server_id = server_id
        self.log = log

    def __repr__(self):
        return '<Server %r>' % self.name


class Csv(db.Model):
    __tablename__ = 'csv'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    demand_number = db.Column(db.String(50), unique=False)
    hostname = db.Column(db.String(50), unique=False)
    csv_path = db.Column(db.String(1024), unique=False)

    def __init__(self, 
                 server_id,
                 demand_number,
                 hostname,
                 csv_path
                 ):
        self.server_id = server_id
        self.demand_number = demand_number
        self.hostname = hostname
        self.csv_path = csv_path

    def __repr__(self):
        return '<Csv %r>' % self.id