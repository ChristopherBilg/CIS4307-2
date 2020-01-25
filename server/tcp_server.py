#!/usr/bin/env python3

import os
import socket
import sys

MAX_CACHE_SIZE = 64000000                    # 64 MB
CONNECTION_BUFFER_SIZE = 1024000000          # 1024 MB
FILE_CACHE = {}
MEMORY_CACHE = {}


# This function will return all of the program parameters
# in an array
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


# This function will repeatedly loop while handling individual connections
# and will only stop when the process itself is stopped
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
                if (os.path.exists(directory + "/" + data)
                        and os.path.isfile(directory + "/" + data)):
                    pass
                else:
                    connection.send(
                        bytearray("Error: File not found", "utf-8")
                    )
                    continue

                # Was found in the 64 MB cache
                if data in FILE_CACHE:
                    print("The requested file was found in the cache")
                    # Send the actual file back and print a message
                    with open(directory + "/" + data, "r") as openedfile:
                        buf = openedfile.read(MEMORY_CACHE[data] * 2)
                        connection.send(bytearray(buf, "utf-8"))
                    print("Sending the requested file")
                # Was NOT found in the 64 MB cache, remove until enough space
                # is found and then add it to the cache
                else:
                    cache_size = 0
                    for key, value in MEMORY_CACHE.items():
                        cache_size += value
                    file_size = os.path.getsize(directory + "/" + data)
                    if file_size < MAX_CACHE_SIZE:
                        for key, value in FILE_CACHE.items():
                            if cache_size + file_size > MAX_CACHE_SIZE:
                                FILE_CACHE.pop(key)
                        FILE_CACHE[data] = 1
                        MEMORY_CACHE[data] = file_size

                        print("The requested file was not found in the cache")
                        print("The requested file was added to the cache")
                        with open(directory + "/" + data) as openedfile:
                            buf = openedfile.read(MEMORY_CACHE[data] * 2)
                            connection.send(bytearray(buf, "utf-8"))
                        print("Sending the requested file")
                    else:
                        print("The requested file was not found in the cache")
                        print("The requested file was too large for the cache")
                        with open(directory + "/" + data) as openedfile:
                            buf = openedfile.read(file_size * 2)
                            connection.send(bytearray(buf, "utf-8"))
                        print("Sending the requested file")
            else:
                # File not found error
                connection.send(bytearray("Error: File not found", "utf-8"))
                print("The requested file was not found")

                return
        finally:
            # Close the connection to this client and loop back
            print("Closing the connection from " + str(client_address))
            connection.close()

    return


# The main function which is called to initiate the program
def main():
    args = parseArguments()
    if args is None:
        return

    handleTCPConnections(args[0], args[1])

    return


# This snippet of code verifies that this file was called through the command
# line and not through another python file. (reduces unnecessary errors)
if __name__ == "__main__":
    main()
