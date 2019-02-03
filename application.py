#!/usr/bin/env python3

import os

compsystem = os.uname()
OnPi = compsystem.nodename == 'raspberrypi'

if OnPi:
    from piCode.streamwrite import pi_client as pi
else:
    from facenet_trials import teststart as fn
    from piCode.streamwrite import computer_server as comp


def runStuff():
    compsystem = os.uname()
    
    if OnPi:
        runPi()
    else:
        runComp()

    return compsystem.nodename

def runComp():
    print("Ready and waiting")

def runPi():
    print("I'm a Pi Pie Phi guy")

if __name__ == "__main__":
    print(runStuff())
