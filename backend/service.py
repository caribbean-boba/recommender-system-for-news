import pyjsonrpc
import os
import sys
import json

from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__), './','helpers'))

import database_client
  
  
def add(a, b):
    """Test function"""
    return a + b

def getNews(self):
    db = database_client.get_db()
    temp = list(db['news'].find())
    return json.loads(dumps(temp))



class RequestHandler(pyjsonrpc.HttpRequestHandler):
    # Register public JSON-RPC methods
    methods = dict(
        add = add
    )

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 4040),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:4040"
try:
    http_server.serve_forever()
except KeyboardInterrupt:
    http_server.shutdown()
print "Stopping HTTP server ..."