#!/user/bin/env python
import socket, sys

def get():
    
    bool = raw_input('Test Get?')

    if bool == 'no' or bool == 'n':
	return -1
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP client ( specified by SOCK_STREAM)
    
        hostName = 'adriatic.cse.msu.edu'
        port       = 8082

        ## initiate TCP connection
        s.connect( (hostName, port) )
        print 'connected to adriatic at port 8082'

        s.send("GET / HTTP/1.0\r\n\r\n")

        #directly from sockets page
        response = ""
        while True:
            buf = s.recv(1000) # buffer size of 1000
            if not buf:
                break
            response += buf

        s.close()

        print 'reponse: ' + response


def form():

    bool = raw_input('Test Form?')

    if bool == 'no' or bool == 'n':
        return -1
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP client ( spe$

        hostName = 'adriatic.cse.msu.edu'
        port       = 8082

        ## initiate TCP connection
        s.connect( (hostName, port) )
        print 'connected to adriatic at port 8082'

        s.send("GET /inventory.html HTTP/1.0\r\n\r\n")

        #directly from sockets page
        response = ""
        while True:
            buf = s.recv(1000) # buffer size of 1000
            if not buf:
                break
            response += buf

        s.close()

        print 'reponse: ' + response


def image():

    bool = raw_input('Test Image?')

    if bool == 'no' or bool == 'n':
        return -1
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP client ( spe$

        hostName = 'adriatic.cse.msu.edu'
        port       = 8082

        ## initiate TCP connection
        s.connect( (hostName, port) )
        print 'connected to adriatic at port 8082'

        s.send("GET /helmet.html HTTP/1.0\r\n\r\n")

        #directly from sockets page
        response = ""
        while True:
            buf = s.recv(1000) # buffer size of 1000
            if not buf:
                break
            response += buf

        s.close()

        print 'reponse: ' + response

if __name__ == '__main__':
    get()
    form()
    image()





