
import urllib.request as urllib2
import socket
import time
import gzip
#import StringIO
from io import StringIO, BytesIO
import re
import random
from bs4 import BeautifulSoup

user_agents = []
class Google_serch_url:
    def __init__(self):
        timeout = 40
        socket.setdefaulttimeout(timeout)
        url_list=[]

    def extractUrl(self, href):
        url = ''
        pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)
        return url

    def extractSearchResults(self, html,url_list):
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', id='main')
        if (type(div) == type(None)):
            div = soup.find('div', id='center_col')
        if (type(div) == type(None)):
            div = soup.find('body')
        if (type(div) != type(None)):
            lis = div.findAll('a')
        if (len(lis) > 0):
            for link in lis:
                if (type(link) == type(None)):
                    continue
                url = link['href']
                if url.find(".google") > 6:
                    continue

                url = self.extractUrl(url)
                if url:
                    url_list.append(url)

        return url_list

    def randomSleep(self):
        sleeptime = random.randint(60, 120)
        time.sleep(sleeptime)

    def search(self, query, lang='tw', num=10,pages=1):
        base_url = "https://www.google.com"
        query += 'site:pixnet.net'
        query = urllib2.quote(query)
        url_list=[]
        for p in range(0, pages):
            url = '%s/search?hl=%s&num=%d&start=%s&q=%s' % (
                base_url, lang, num, p, query)
            try:
                request = urllib2.Request(url)
                length = len(user_agents)
                index = random.randint(0, length - 1)
                user_agent = user_agents[index]
                request.add_header('User-agent', user_agent)
                request.add_header('connection', 'keep-alive')
                request.add_header('Accept-Encoding', 'gzip')
                request.add_header('referer', base_url)
                response = urllib2.urlopen(request)
                html = response.read()
                if (response.headers.get('content-encoding', None) == 'gzip'):
                    html = gzip.GzipFile(
                        fileobj=BytesIO(html)).read()

                url_list = self.extractSearchResults(html,url_list)
                
                
            except urllib2.URLError as e:
                print('url error:', e)
                self.randomSleep()
                continue

            except Exception as e:
                print('error:', e)
                self.randomSleep()
                continue
                
        return url_list
def load_user_agent():
    agents=[]
    fp = open('./user_agents', 'r')
    line = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()
    return agents

def crawler(key_list=['雞胸肉'],num=10,pages=1):
    results=[]
    load_user_agent()
    api=Google_serch_url()
    for i in key_list:
        url_list = api.search(i,num=num,pages=pages)
        results.append(url_list)
    return results


if __name__ == '__main__':

    crawler()

