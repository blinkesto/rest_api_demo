#!/bin/env python

import ConfigParser
import argparse
import os
import requests


class MyConfig():
    Config = None

    def __init__(self, config_file):
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(config_file)

    def read(self, section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

class Build():
    id = None
    num = None
    url = None
    config = None

    def __init__(self, config_file):
        self.config = MyConfig(config_file)
        self.url = "%s://%s:%s%s" % (self.config.read("tilt")['proto'], 
                                      self.config.read("tilt")['host'], 
                                      self.config.read("tilt")['port'], 
                                      self.config.read("builds")['url'])

    def add(self, build_num):
        self.num = build_num
        print "Build.add: Adding build NUM: %s to %s" % (self.num, self.url)
        build_data={'number':build_num, 'servers':[]}
        response = requests.post(self.url, json=build_data)
        print(response.text)
        if response:
            return 0
        else:
            return 1
        
class Server():
    id = None
    name = None
    status = None
    build_id = None

    def __init__(self, args):
        self.config = MyConfig(args.config_file)
        self.url = "%s://%s:%s%s" % (self.config.read("tilt")['proto'],
                                      self.config.read("tilt")['host'],
                                      self.config.read("tilt")['port'],
                                      self.config.read("servers")['url'])

    def add(self, args):
        self.name = args.name
        self.status = args.status
        self.build_id = args.build_id

        print "Server.add: Adding server NAME: %s to %s" % (self.name, self.url)
        _data={'name': self.name, 'status': self.status, 'build_id': self.build_id }
        response = requests.post(self.url, json=_data)
        if response:
            return 0
        else:
            return 1        

# Argparse helpers
def add_build(args):
    print "Adding build: %s" % args.build_num
    build = Build(args.config)
    build.add(args.build_num)

def add_server(args):
    print "Adding server: %s" % args.name
    server = Server(args)
    server.add()

def info():
    print "Usage: do_build [build_num]"

def _get_parser():
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers(help='sub-command help')

    parser_create_build = subparsers.add_parser('add_build', help='Add a build')
    parser_create_build.set_defaults(func=add_build)
    parser_create_build.add_argument("--config", help="Client config file")
    parser_create_build.add_argument("--build_num", help="Number of the build")

    parser_create_server = subparsers.add_parser('add_server', help='Add a server')
    parser_create_server.set_defaults(func=add_server)
    parser_create_server.add_argument("--config", help="Client config file")
    parser_create_server.add_argument("--name", help="Name of the server")
    parser_create_server.add_argument("--ip", help="IP of the server")

    parser_info = subparsers.add_parser('info', help='Shows usage info')
    parser_info.set_defaults(func=info)

    return main_parser

def command_line_runner():
    parser = _get_parser()
    args = parser.parse_args()
  
    # parse the args and call whatever function was selected
    args.func(args)
    

if __name__ == '__main__':
    command_line_runner()

