from googlesearch import crawler, load_user_agent
import random
import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm


class pixnet:
    def __init__(self):
        self.flatten = lambda l: [item for sublist in l for item in sublist]
        self.data = {}
        self.user_agents = load_user_agent()

    def filter_str(self, text, key, pattern="[https]{4,5}:\/\/[0-9a-zA-Z.\/].*"):
        text_clean = ''.join(re.split(pattern, text))
        # text_clean = ''.join(re.split(r'[\W]*', text_clean))
        text_clean = ''.join(re.split(r'由', text_clean))
        text_clean = ''.join(re.split(r'痞客邦', text_clean))
        text_clean = ''.join(re.split(r'原始評論', text_clean))
        text_clean = ''.join(re.split(r'Google', text_clean))
        text_clean = ''.join(re.split(r'\n', text_clean))
        text_clean = ''.join(re.split(r'\s', text_clean))
        res = re.compile(f"[^\\u4e00-\\u9fa5，^0-9。!?^{key}]+")
        text_clean = res.sub('', text_clean)
        return text_clean

    def fetch_soup(self, url):
        try:
            length = len(self.user_agents)
            index = random.randint(0, length - 1)
            user_agent = self.user_agents[index]
            html = requests.get(url, headers={
                'User-Agent': user_agent}, timeout=5)
            html.encoding = 'utf-8'
            soup = BeautifulSoup(html.text, 'lxml')
        except:
            soup = BeautifulSoup('0')
        return soup

    def fetch_article(self, soup, key):
        a = []
        keyword_list = []
        for i in soup.find_all("p"):
            word = self.filter_str(i.text, key)
            if len(word) > 20 and word not in a:
                a.append(word)
        for k in soup.find_all("a", "tag"):
            keyword_list.append(k.text.replace('\n', ''))
        return a, keyword_list

    def main(self, key=['雞胸肉'], num=10, pages=1):
        url_list = crawler(key, num, pages)
        for i, v in enumerate(url_list):
            act = []
            keyword_list = []
            for url in tqdm(v, ascii=True, desc=f"{key[i]}"):
                soup = self.fetch_soup(url)
                if soup.text == '0':
                    continue
                a, keywords = self.fetch_article(soup, key[i])
                act.append(a)
                keyword_list.append(keywords)
            self.data[key[i]] = {'article': self.flatten(act), 'keywords': list(set(self.flatten(keyword_list)))}
        return self.data

