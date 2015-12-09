#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import imp
import socket
import time
import urllib2
import re
import types
import pickle
from ConfigParser import RawConfigParser
import Parser

PI = 3.14159265
connection = 1
DEBUG = 0
ircsock = None
socket.setdefaulttimeout(600.0)

def getConfigDict():

    cParser = RawConfigParser()
    cParser.read('conf.cfg')

    config = {
    'server' : cParser.get('connection','con'),
    'channels' : cParser.get('bot','channels').split(','),
    'botnick' : cParser.get('bot','nick'),
    'mode' : cParser.get('bot','mode'),
    'realname' : cParser.get('bot','realname')}

    return config


def joinchan(chan, password=""):
    ircsock.send("JOIN " + chan + password + "\r\n")

def main(argv=None):
    global DEBUG, gamelist, ircsock
    if argv is None:
        argv = sys.argv
    
    if 'debug' in argv:
        DEBUG = 1

    config = getConfigDict()
    
    if DEBUG == 0:
        ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ircsock.connect((config['server'], 6667))
        time.sleep(0.5)
        ircsock.send("USER " + config['botnick'] + " " + config['mode'] + " * :%s\r\n" %(config['realname']))
        time.sleep(0.5)
        ircsock.send("NICK " + config['botnick'] + "\r\n")

        for channel in config['channels']:
            joinchan(channel)
    else:
        print("succesfully connected")

    while connection == 1:
        if DEBUG == 0:
            ircmsg = ircsock.recv(2048)
            ircmsg = ircmsg.strip('\n\r')
        else:
            ircsock = None
            ircmsg = "%s" %raw_input('debug: ')
        
        print(ircmsg)
        
        msglist = Parser.parse(ircmsg)
        
        if msglist is None:
            continue
        if msglist[0] == 'reload':
            imp.reload(Parser)
        elif msglist[0] == 'ERROR':
            print msglist[0]
        else:
            if DEBUG == 0:
                for msg in msglist:
                    ircsock.send('{}\r\n'.format(msg.encode("utf-8", "ignore")))
            else:
                for msg in msglist:
                    print(msg)

if __name__ == '__main__':

    while 1:
        try:
            main(sys.argv)
        except Exception as e:
            print e
            time.sleep(15)

#eof



