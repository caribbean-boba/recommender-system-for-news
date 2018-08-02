from message_client import MessageClient

URL = "amqp://pcmwjrjr:Ztb_W2cjJF5AJqyYTLzU0e5tzvcCxnd8@lion.rmq.cloudamqp.com/pcmwjrjr"
NAME = 'test_1'

def test_basic():
    print ("start test")
    client = MessageClient(URL, NAME)
    sentMess = {'test_1': '1'}
    client.sendMessage(sentMess)
    client.sleep(10)
    receiveMess = client.getMessage()
    assert sentMess == receiveMess
    print ("pass test")

if __name__ == "__main__":
    test_basic()