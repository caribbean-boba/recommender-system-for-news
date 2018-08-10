import pyjsonrpc

client = pyjsonrpc.HttpClient("http://localhost:6060/")

def classify(text):
    topic = client.call('classify', text)
    print str(topic)
    return topic