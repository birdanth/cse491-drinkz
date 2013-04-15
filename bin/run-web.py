#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson

import sys
import _mypath

from drinkz.app import SimpleApp

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
