import cnn_scraper as scraper

EXPECTED_STRING = "President Donald Trump has been urged to stop tweeting about the 2016 Trump Tower meeting"
CNN_NEWS_URL = "https://us.cnn.com/2018/08/06/politics/donald-trump-trump-tower-meeting/index.html"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)

    assert EXPECTED_STRING in news
    # print news
    print 'test_basic passed!'

if __name__ ==  "__main__":
    test_basic()