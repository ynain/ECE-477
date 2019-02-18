#!/usr/bin/env python3

import signal
import sys

def closeSocket(conn, recv, send):
    def signal_handler(sig, frame):
        print("\nCtrl+C signal sensed!\nClosing the socket...")
        
        for el in [conn, recv, send]:
            try:
                el.close()
            except Exception as e:
                print("Possibly already closed...")
            finally:
                print("")

        print("All closed. Buh-bye!")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)