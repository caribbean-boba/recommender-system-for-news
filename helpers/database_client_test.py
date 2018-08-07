import database_client as client

def test_basic():
    db = client.get_db('news')
    print db.news.count()
    assert db.news.count() == 1495
    print ('passed')

if __name__ == "__main__":
    test_basic()