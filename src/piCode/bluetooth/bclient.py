from bluetooth import *

# Create the client socket
client_socket=BluetoothSocket( RFCOMM )

client_socket.connect(("b8:27:eb:2f:e1:ba", 3))

client_socket.send("Hello World")

print("Finished")

client_socket.close()
