#!/usr/bin/env python3

import socket

from src.piCode.streamwrite import pi_client as pstr

def getConnection():
    pass

def getWriteSocs(connection):
    pass

def sendFrames(connect=None):
    pass

def readResults(connect=None):
    pass

def closeWriteFiles(send, recv):
    send.close()
    recv.close()

def closeConnection(connection):
    connection.close()