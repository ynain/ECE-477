

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


def bluetoothSkeleton(ipaddress='10.3.141.198', port=8000):
    print("Pi Pie Phi guy running")

    command = ''
    bsock = None
    while command != 'quit':
        try:
            if bsock is None:
                # connect to Bluetooth
                bsock = pi.getBlueConnection(mac="98:D3:71:FD:50:9E")

            # wait for "boot\n"? Also, testing, HC-05 stuck in stasis
            # if here, likely lost bluetooth connection, so wait to boot up again
            while not pi.waitForBlueMessage(bsock, "boot")[0] and not pi.waitForBlueMessage(bsock, "start")[0]:
                continue

            # send ready, pretend server connected
            pi.sendBlueMessage(bsock, "c")
                

            while command != 'quit':
                send = recv = None                
                try:
                    found = None
                    while found is None:
                        success, found = pi.waitForBlueMessage(bsock, "start", timeout=4)
                        if not success:
                            success, found = pi.waitForBlueMessage(bsock, "lowpwr", timeout=4)
                    
                    if success:
                        if found == "lowpwr":
                            pi.closeBluetoothConnection(bsock)
                            break
                        
                        respass = True
                        # randomize response, 10% chance for simulated output failure
                        if random.random() > .9:
                            respass = False
                        
                        pi.sendResBluetooth(respass, bsock)

                except blt.BluetoothError as bterr:
                    # if lost bluetooth, set blue to None, reconnect, wait for start/boot?
                    traceback.print_exc()
                    print("Bluetooth failed, connecting again")
                    
                    pi.closeBluetoothConnection(bsock)

                    bsock = None
                    break
                    

                except Exception as e:
                    traceback.print_exc()
                    break
            
                command = input("Type anything to send images again,\n or 'quit' to quit\n")

        except Exception as e:
            traceback.print_exc()

        finally:
            if command == 'quit':
                break
            command = input("Main connection failure, type 'quit' not to retry\n")

    print("{} entered".format(command))

if __name__ == "__main__":
    runPi(ipaddress='10.3.141.198')
    # runPi(ipaddress='10.186.129.210')
