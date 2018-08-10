import pyjsonrpc

URL = "http://localhost:5050/"

client = pyjsonrpc.HttpClient(url=URL)

def getPreferenceForUser(userId):
    print ("yeah!!!!!")
    return client.getPreferenceForUser(userId)