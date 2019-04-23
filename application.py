

#import bluetooth as blt
import traceback
import socket
import struct
import sys
import os

# Project is built using Python 3.5+, please comply
if sys.version_info[0] < 3:
    sys.exit('''Project is built using Python 3.5+\n'''
             '''Please comply or this won't work properly'''
             )

compsystem = os.uname()
OnPi = compsystem.nodename == 'raspberrypi'

if OnPi:
    import src.pi_run as pi
    import bluetooth as blt
else:
    import src.comp_run as cr
    
import src.helpers as h

def runComputer(writeImagePath=None, rot=False):
    known = cr.getKnownFaces()
    while True:
        conn, _ = cr.getServerConnection()

        while True:
            send = recv = None
            try:
                send, recv = cr.getWriteSocs(conn)
                h.catchInterruptClose(conn, recv, send)

                images = cr.getImages(connect=recv, log=False)

                # For our orientation during testing, images need to be corrected
                # The face_recognition library can't see faces that aren't upright
                if rot:
                    images = cr.rotList(images)

                if not writeImagePath is None:
                    cr.writeImages(images, writeImagePath)
                
                if len(images):
                    res = cr.getResults(images, known)

                    cr.sendResults(res, connect=send, log=False)
            
            except socket.error as serror:
                traceback.print_exc()
                cr.closeAllSocs(conn, recv, send)

            
            except Exception:
                traceback.print_exc()
                print("Breaking")
                break
            
            if not send is None or not recv is None:
                cr.closeWriteSocs(send, recv)
        
        cr.closeConnection(conn)
    
def runPi(ipaddress='10.3.141.198', port=8000):
    print("Pi Pie Phi guy running")

    command = ''
    conn = None
    bsock = None
    while command != 'quit':
        try:
            if bsock is None:
                # connect to Bluetooth
                bsock = pi.getBlueConnection(mac="98:D3:71:FD:50:9E")

                # wait for "boot\n"? Also, testing, HC-05 stuck in stasis
                # if here, likely lost bluetooth connection, so wait to boot up again
                pswd = "12345678\n"
                received = ""

                while "boot" not in received:
                    if "pswd" in received:
                        print("{} called, sending {}".format("pswd", pswd))
                        pi.sendBlueMessage(bsock, pswd)

                    received = pi.getBlueMessage(bsock)

            if conn is None:
                # wait for "boot\n"? Also, testing, HC-05 stuck in stasis
                while "boot" not in received:
                    received = pi.getBlueMessage(bsock)
                # print("Got boot")
                # connect to server
                conn = pi.getServerConnection(ipaddress=ipaddress)
                # send ready after
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
                    send, recv = pi.getWriteSocs(conn)
                    h.catchInterruptClose(conn, recv, send)
                    pi.sendFrames(connect=send)

                    res = pi.readResults(connect=recv)
                    respass = pi.evaluateImages(res)
                    pi.sendResBluetooth(respass, bsock)
                    print("{} sent".format(respass))
                else:
                    continue
        
            if not send is None or not recv is None:
                pi.closeWriteSocs(send, recv)
        
            pi.closeConnection(conn)
        
        except blt.BluetoothError as bterr:
            # if lost bluetooth, set blue to None, reconnect, wait for start/boot?
            traceback.print_exc()
            print("Bluetooth failed, connecting again")
            
            pi.closeBluetoothConnection(bsock)

            bsock = None

        except socket.error as serror:
            # if lost server, send "l"ost, set conn to None reconnect, send "r"eady after
            traceback.print_exc()
            pi.sendBlueMessage(bsock, "l")
            print("taking an l")
            
            # try to healthily close everything
            pi.closeAllSocs(conn, recv, send)
            
            conn = None
        
        except Exception as e:
            traceback.print_exc()

        finally:
            if command == 'quit':
                break
            command = input("Main connection failure, type 'quit' not to retry\n")

    print("{} entered".format(command))

if __name__ == "__main__":
    if OnPi:
        runPi(ipaddress='10.42.0.1')
        # runPi(ipaddress='10.186.129.210')
    else:
        runComputer()
