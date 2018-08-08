import pyjsonrpc
import os
import sys
import json

from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__), '../','helpers'))

import database_client
import operations
  

def add(a, b):
    """Test function"""
    return a + b

def getNewsSummariesForUser(user_id, page_num):
    print("get_news_summaries_for_user is called with %s and %s" % (user_id, page_num))
    return operations.getNewsSummariesForUser(user_id, page_num)



class RequestHandler(pyjsonrpc.HttpRequestHandler):
    # Register public JSON-RPC methods
    methods = dict(
        add = add,
        getNewsSummariesForUser = getNewsSummariesForUser,
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