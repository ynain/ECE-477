

#import bluetooth as blt
import traceback
import socket
import struct
import random
import sys
import os

compsystem = os.uname()
OnPi = compsystem.nodename == 'raspberrypi'

if not OnPi:
    sys.exit(   '''This test script was made to test Bluetooth, '''
                '''and thus must be run on the Pi. Sorry friend.\n'''
             )

# Project is built using Python 3.5+, please comply
if sys.version_info[0] < 3:
    sys.exit('''Project is built using Python 3.5+\n'''
             '''Please comply or this won't work properly'''
             )

import src.pi_run as pi
import bluetooth as blt
import src.helpers as h


def bluetoothSkeleton(ipaddress='10.3.141.198', port=8000, MAC="98:D3:71:FD:50:9E"):
    print("Pi Pie Phi guy running")

    command = ''
    bsock = None
    while command != 'quit':
        try:
            if bsock is None:
                # connect to Bluetooth
                bsock = pi.getBlueConnection(mac=MAC)

            # wait for "boot\n"? Also, testing, HC-05 stuck in stasis
            # if here, likely lost bluetooth connection, so wait to boot up again
            pswd = "12345678\n"
            received = ""

            while "boot" not in received:
                if "pswd" in received:
                    print("{} called, sending {}".format("pswd", pswd))
                    pi.sendBlueMessage(bsock, pswd)

                received = pi.getBlueMessage(bsock)
            print("Boot received")

            print("Connecting...")
            # send ready, pretend server connected
            pi.sendBlueMessage(bsock, "c")
            print("c sent")
            
            received = ""
            while 'lowpwr' not in received:
                received = pi.getBlueMessage(bsock)
                send = recv = None
                
                if "lowpwr" in received:
                    pi.closeBluetoothConnection(bsock)
                    bsock = None
                    break
                
                elif "start" in received:
                    respass = True
                    ran = random.random()
                    # randomize response, 10% chance for simulated output failure
                    if ran > .7:
                        pi.sendBlueMessage(bsock, "l")
                        break
                    elif ran > .35:
                        respass = False
                        pi.sendResBluetooth(respass, bsock)
                    else:
                        respass = True
                        pi.sendResBluetooth(respass, bsock)
        
        except blt.BluetoothError as bterr:
            # if lost bluetooth, set blue to None, reconnect, wait for start/boot?
            traceback.print_exc()
            print("Bluetooth failed, connecting again")
            
            pi.closeBluetoothConnection(bsock)

            bsock = None

        except Exception as e:
            traceback.print_exc()

        finally:
            if command == 'quit':
                break
            command = input("Main connection failure, type 'quit' not to retry\n")

    print("{} entered".format(command))

if __name__ == "__main__":
    bluetoothSkeleton(ipaddress='10.3.141.198')
    # bluetoothSkeleton(ipaddress='10.186.129.210')
