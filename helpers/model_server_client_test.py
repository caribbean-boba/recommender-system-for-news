import model_server_client as client

def test_basic():
    newsTitle = "Pentagon might propose ground troops for Syria"
    topic = client.classify(newsTitle)
    assert topic == "U.S."
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()