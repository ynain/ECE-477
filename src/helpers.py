#!/usr/bin/env python3

import signal
import sys

def catchInterruptClose(conn, recv, send):
    def signal_handler(sig, frame):
        print("\nCtrl+C signal sensed!\nClosing the socket...")
        
        closeAll([conn, recv, send])

        print("All closed. Buh-bye!")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

def closeAll(els):
    for el in els:
        try:
            el.close()
        except Exception as e:
            print("Possibly already closed...")
        finally:
            print("")