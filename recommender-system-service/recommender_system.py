import operator
import os
import sys

import pyjsonrpc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'helpers'))

import database_client

PREFERENCE_MODEL_TABLE = "user_preference_model"

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def getPreferenceForUser(user_id):
    """ Get user's preference in an ordered class list """
    print ("userid: %s" % user_id)
    db = database_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE].find_one({'user_id':user_id})
    print ('model')
    print (model)
    if model is None:
        return []

    sorted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)
    sorted_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]

    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []

    return sorted_list

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    # Register public JSON-RPC methods
    methods = dict(
        isclose = isclose,
        getPreferenceForUser = getPreferenceForUser,
    )

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 5050),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server ..."
print "URL: http://localhost:5050"
try:
    http_server.serve_forever()
except KeyboardInterrupt:
    http_server.shutdown()
print "Stopping HTTP server ..."