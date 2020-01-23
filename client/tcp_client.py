#!/usr/bin/env python3

import socket
import sys


CONNECTION_BUFFER_SIZE = 1024000000    # 1024 MB

def requestFileOverTCPConnection(server_host, port, filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_host, port)

    print("Attempting to open a connection with "
          + str(server_host)
          + ":"
          + str(port))
    s.connect(server_address)
    print("Successfully opened a connection with "
          + str(server_host)
          + ":"
          + str(port))

    s.send(bytearray(filename, "utf-8"))
    message = s.recv(CONNECTION_BUFFER_SIZE)
    if not message:
        print("Error: received message corrupted")
        exit

    # TODO: Here should not print the message, but rather save the file in the local directory
    print(str(message))
    
    return

def parseArguments():
    argumentLength = len(sys.argv)
    if argumentLength < 4:
        print("Correct syntax: "
              + sys.argv[0]
              + " <server_host> <server_port> <filename>")
        return None

    arguments = []
    arguments.append(str(sys.argv[1]))
    arguments.append(int(sys.argv[2]))
    arguments.append(str(sys.argv[3]))
    
    return arguments

def main():
    args = parseArguments()
    if args is None:
        return

    requestFileOverTCPConnection(args[0], args[1], args[2])
    
    return

if __name__ == "__main__":
    main()
