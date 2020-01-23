#!/usr/bin/env python3

import socket
import sys

MAX_CACHE_SIZE = 64                    # 64 MB
CONNECTION_BUFFER_SIZE = 1024000000    # 1024 MB


def parseArguments():
    argumentLength = len(sys.argv)
    if argumentLength < 3:
        print("Correct syntax: "
              + sys.argv[0]
              + " <port_to_listen_on> <file_directory>")
        return None

    arguments = []
    arguments.append(int(sys.argv[1]))
    arguments.append(str(sys.argv[2]))
    
    return arguments

def handleTCPConnections(port, directory):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', port)

    s.bind(server_address)
    s.listen()

    while True:
        print("Waiting to establish a connection")
        connection, client_address = s.accept()

        try:
            print("Attempting to open connection from " + str(client_address))
            data = connection.recv(CONNECTION_BUFFER_SIZE)
            if data:
                # TODO: Check for cache hit or miss, also check for if the file even exists, also send the actual file
                data = data.decode('utf-8').strip('\r\n')
                connection.send(bytearray(data, "utf-8"))
                print("Sending the requested file")
            else:
                connection.send(bytearray("Error: File not found", "utf-8"))
                print("The requested file was not found")
                
                return
        finally:
            print("Closing the connection from " + str(client_address))
            connection.close()
    
    return

def main():
    args = parseArguments()
    if args is None:
        return

    handleTCPConnections(args[0], args[1])
    
    return

if __name__ == "__main__":
    main()
