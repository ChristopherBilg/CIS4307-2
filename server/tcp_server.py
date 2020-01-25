#!/usr/bin/env python3

import os
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
                data = data.decode("utf-8").strip("\r\n")

                # Check if the file exists, if not send back an error message
                if os.path.exists(directory + "/" + data) and os.path.isfile(
                        directory + "/" + data
                ):
                    pass
                else:
                    connection.send(
                        bytearray("Error: File not found", "utf-8")
                    )
                    continue

                # TODO: Check for a cache hit or miss, and implement it (64 MB)

                # Send the actual file back and print a message on the server
                with open(directory + "/" + data, "r") as openedfile:
                    buf = openedfile.read(CONNECTION_BUFFER_SIZE)
                    connection.send(bytearray(buf, "utf-8"))
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
