# CIS4307-2
CIS 4307 - Network Communication

## Program Overview Explanation
The program consists of two python files. Those are server/tcp_server.py and client/tcp_client.py. They both run on the python 3.6+ platform. In order to start and use the client and server files, you should begin by running the following command: "python3 tcp_server.py 10001 files/"

In a separate terminal, you can next run the following command, and feel free to change the "test.txt" parameter: "python3 tcp_client.py 127.0.0.1 10001 test.txt"

You will see that the client will send the filename to the server, then the server will process the filename and verify that the file exists before sending the file back to the client. If the file does not exist then an error message is sent back to the client and the client will display the error message given. All of the communication steps have command line prompts that will tell you, the user, what is happening and in what order it is happening.

## Cache Implementation Details
The 64 MB cache that I implemented consists of two parts. First, a dictionary of filename and file contents. Secondly, a dictionary consisting of filename and file size. Both of these dictionary work hand in hand to ensure that if a file is requested, the server will first check the cache for the file. If the file is in the cache then the server will send the file over to the client. If the file is not in the memory cache, then enough space in the cache is made for the file and the file is added to the cache before being sent over to the client.

## Test Cases Used
I used many manual test cases for this assignment. Some of the tests that I performed included; sending a filename to the server that I knew did not exist, sending a filename to the server that I knew was not in the cache, sending a filename to the server that was currently in the cache, sending a filename to the server that was too large to fit into the cache, and send a filename to the server that was not in the cache but that could fit into the cache.

As for error handling, I believe that I gracefully handled all possible errors that can be thrown by this program. Those include but are not limited to; file not found errors, file too large errors (cache), and file too large errors (TCP connection).