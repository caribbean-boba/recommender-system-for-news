import requests
from json import loads
ENDPOINT = 'https://newsapi.org/v2/'
KEY = 'd650981e4c624bc6868d82a810f850af'
SROURCE_LIST = ['cnn']

def getNews(sources = SROURCE_LIST, sortBy = 'top'):
    print sources
    sources = sources.split(',')
    results = []
    for source in sources:
        payload = {'apiKey': KEY, 'sources': source}
        res = requests.get(buildUrl(), params = payload)
        # print res['articles']
        res = loads(res.content.decode('utf-8'))
        # print res
        if (res is not None and res['status'] == 'ok'):
            print "success"
            # print res['articles']
            # for news in res['artical']:
            #     news['source'] = res['source']
            # results + [x for x in res['articles'] if x not in results]
            results.extend(res['articles'])
    return results


def buildUrl(end_point = ENDPOINT, api_name = 'top-headlines'):
    return end_point+api_name