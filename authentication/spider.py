import requests
import re
from faker import Faker
from lxml import etree


class CrawlProject(object):
    """ 从网上爬取昵称，用于用户注册时随机生成他的昵称 """
    nickname_ls = []

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.request_url()

    def request_url(self):
        """ 发送请求 """
        response = requests.get(url=self.url, headers=self.headers)
        response.encoding = 'gbk'
        self.parse_html(content=response.text)

    def parse_html(self, content):
        """ 解析数据 """
        html = etree.HTML(content)
        p_ls = html.xpath('//div[@id="content"]/p[position()>1][position()<=400]/text()')
        for p in p_ls:
            p = p.strip().replace('、', '')
            p_res = re.search(r'^[0-9]*(.*)', p).group(1)
            if len(p_res) <= 8:
                self.nickname_ls.append(p_res)


if __name__ == '__main__':
    headers = {
        'User-Agent': Faker().user_agent()
    }
    crawl = CrawlProject(url='https://www.qunzou.com/wangming/11052.html', headers=headers)
    print(crawl.nickname_ls, len(crawl.nickname_ls))
