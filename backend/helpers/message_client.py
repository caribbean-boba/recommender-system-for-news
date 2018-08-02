import pika
import json
class MessageClient:
    def __init__(self, url, queue_name):
        self.url = url
        self.queue_name = queue_name
        self.params = pika.URLParameters(url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = queue_name)
    def sendMessage(self, message):
        self.channel.basic_publish(exchange='', routing_key = self.queue_name, body = json.dumps(message))
        print ("sent message to %s: %s" % (self.queue_name, message))
        return
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame is not None:
            print ("received message from %s: %s" % (self.queue_name, body))
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            return None
    def sleep(self, seconds):
        self.connection.sleep(seconds)
