import collections
import json

import scrapy


class PjSpider(scrapy.Spider):
    name = 'pj'
    allowed_domains = ['bgm.tv']
    f = open('ysj2021.json', 'a', encoding='utf-8')
    start_urls = []
    for i in range(1, 23):
        start_urls.append('https://bgm.tv/subject/302190/comments?page=' + str(i))


    def parse(self, response):
        comm = response.xpath('//div[@class=\'item clearit\']')
        for x in comm:
            commit = x.xpath('div/div/p/text()').extract()
            commits = str(commit)
            comment = commits.strip('\r\n').strip('\n').replace('\r\n', ' ').replace('\n', ' ').replace\
                ('\\\\n', ' ').replace('//', ' ').replace('\\n', ' ').replace('=', ' ').replace('@', ' ')
            cur = collections.OrderedDict()
            cur['comment'] = comment
            ss = json.dumps(cur, ensure_ascii=False)
            self.f.write(str(str(ss)) + '\n')
