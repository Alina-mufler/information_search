import re
import sys

from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import os

sys.path.append('../')
my_path = os.path.abspath('')


def get_links():
    parser = 'html.parser'
    links = ["https://briefly.ru/dostoevsky/prestuplenie/", "https://www.chitalnya.ru/public_prose_list.php"]
    for link in links:
        resp = requests.get(link)
        http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
        encoding = html_encoding or http_encoding
        soup = BeautifulSoup(resp.content, parser, from_encoding=encoding)
        with open('list_links.txt', 'a', encoding='utf-8') as list_links_file:
            for l in soup.find_all('a', href=True):
                if not re.search('http(.)*', l.__str__()):
                    list_links_file.write(link[:-1] + l['href'] + '\n')


def get_html():
    num = 0
    with open('list_links.txt', 'r', encoding='utf-8') as list_links_file:
        for link in list_links_file:
            try:
                resp = requests.get(link)
                soup = BeautifulSoup(resp.content, "html.parser")
                if num <= 100:
                    with open('index.txt', 'a', encoding='utf-8') as index:
                        index.write('{} -- {}'.format(num, link))
                    with open('./list_html/{}.html'.format(num), 'w', encoding='utf-8') as f:
                        f.write(str(soup.prettify()))
                        num += 1
                else:
                    break
            except (ConnectionError, BaseException) as e:
                pass


if __name__ == '__main__':
    if not os.path.exists('list_links.txt'):
        get_links()
    get_html()

