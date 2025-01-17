#!/usr/bin/env python3

import os
import socket
import sys

CONNECTION_BUFFER_SIZE = 1024000000    # 1024 MB


# This function will send a message to the server requesting
# a specific file name
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
        print("Error: received message was corrupted")
        exit

    # Save the file to the local directory
    if os.path.exists(filename):
        os.remove(filename)
    if not message.decode("utf-8").lower().startswith("error:"):
        with open(filename, "w") as openedfile:
            openedfile.write(message.decode("utf-8"))
        print("Successfully saved the file")
    else:
        print(message.decode("utf-8"))

    return


# This function, much like that in the tcg_server.py file, will return
# an array of the program parameters
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


# This function will be called to initiate the client itself
# and will handle the connection with the server and the file passing
def main():
    args = parseArguments()
    if args is None:
        return

    requestFileOverTCPConnection(args[0], args[1], args[2])

    return


# This snippet of code verifies that this file was called through the command
# line and not through another python file. (reduces unnecessary errors)
if __name__ == "__main__":
    main()
