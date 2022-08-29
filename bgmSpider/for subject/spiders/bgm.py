# coding=utf-8
import collections
import json
import sys
import scrapy
import importlib, sys

importlib.reload(sys)


class subject(scrapy.spiders.Spider):
    f = open('subjecttt.json', 'a', encoding='utf-8')
    error = open('subject_errortt.txt', 'a', encoding='utf-8')
    name = 'bgm'
    start_urls = []

    for i in range(335570, 335589):
        start_urls.append('https://bgm.tv/subject/' + str(i))

    def parse(self, response):
        id = response.url
        id = id[id.rfind('/') + 1:]
        message = response.xpath('//*[@id="colunmNotice"]/div/h2/text()').extract()
        if len(message) != 0:
            self.error.write(id + '\n')
            self.error.flush()
            return

        sub_cat = response.xpath('//a[@class="focus chl"]/@href').extract()
        if len(sub_cat) == 0:
            sub_cat = response.xpath('//a[@class="focus chl anime"]/@href').extract()
        if len(sub_cat) == 0:
            sub_cat = response.xpath('//a[@class="focus chl real"]/@href').extract()
        if len(sub_cat) == 0:
            self.error.write('--------' + id + '\n')
            self.error.flush()
            return
        sub_cat = sub_cat[0]
        sub_cat = sub_cat[1:]

        tag = response.xpath('//div[@class="subject_tag_section"]/div/a/span/text()').extract()
        img = response.xpath('//div[@id="bangumiInfo"]/div/div/a/img/@src').extract()
        namechs = response.xpath(u'//span[./text()="中文名: "]/following::text()[1]').extract()
        nameor = response.xpath('//h1[@class="nameSingle"]/a/text()').extract()
        cat = response.xpath('//h1[@class="nameSingle"]/small/text()').extract()
        star = response.xpath('//span[@class="number"]/text()').extract()
        rank = response.xpath('//small[@class="alarm"]/text()').extract()
        if len(rank) == 1:
            rank[0] = rank[0][1:]
        votes = response.xpath('//div[@id="ChartWarpper"]/div/small/span/text()').extract()

        all = []
        allkey = []

        if sub_cat == 'anime':
            eps = response.xpath(u'//span[./text()="话数: "]/following::text()[1]').extract()
            date = response.xpath(u'//span[./text()="放送开始: "]/following::text()[1]').extract()
            if len(date) == 0:
                date = response.xpath(u'//span[./text()="上映年度: "]/following::text()[1]').extract()
            if len(date) == 0:
                date = response.xpath(u'//span[./text()="发售日: "]/following::text()[1]').extract()
            author = response.xpath(u'//span[./text()="原作: "]/following::text()[1]').extract()
            director = response.xpath(u'//span[./text()="导演: "]/following::text()[1]').extract()
            storyboard = response.xpath(u'//span[./text()="分镜: "]/following::text()[1]').extract()
            storyset = response.xpath(u'//span[./text()="脚本: "]/following::text()[1]').extract()
            personset = response.xpath(u'//span[./text()="人物设定: "]/following::text()[1]').extract()
            all = [namechs, nameor, cat, eps, date, star, rank, votes, author, director, storyboard,
                   storyset, personset, img]
            allkey = ['namechs', 'nameor', 'cat', 'eps', 'date', 'star', 'rank', 'votes', 'author', 'director',
                      'storyboard', 'storyset', 'personset', 'img']
        elif sub_cat == 'book':
            eps = response.xpath(u'//span[./text()="话数: "]/following::text()[1]').extract()
            date = response.xpath(u'//span[./text()="发售日: "]/following::text()[1]').extract()
            painter = response.xpath(u'//span[./text()="作画: "]/following::text()[1]').extract()
            author = response.xpath(u'//span[./text()="作者: "]/following::text()[1]').extract()
            pub = response.xpath(u'//span[./text()="出版社: "]/following::text()[1]').extract()
            pages = response.xpath(u'//span[./text()="页数: "]/following::text()[1]').extract()
            all = [namechs, nameor, cat, eps, date, star, rank, votes, painter, author, pub, pages, img]
            allkey = ['namechs', 'nameor', 'cat', 'eps', 'date', 'star', 'rank', 'votes', 'painter', 'author',
                      'pub', 'pages', 'img']
        elif sub_cat == 'music':
            date = response.xpath(u'//span[./text()="发售日期: "]/following::text()[1]').extract()
            artist = response.xpath(u'//span[./text()="艺术家: "]/following::text()[1]').extract()
            all = [namechs, nameor, cat, date, star, rank, votes, artist, img]
            allkey = ['namechs', 'nameor', 'cat', 'date', 'star', 'rank', 'votes', 'artist', 'img']
        elif sub_cat == 'game':
            date = response.xpath(u'//span[./text()="发售日: "]/following::text()[1]').extract()
            if len(date) == 0:
                date = response.xpath(u'//span[./text()="发行日期: "]/following::text()[1]').extract()
            platform = response.xpath(u'//span[./text()="平台: "]/following::text()[1]').extract()
            for i in range(1, len(platform)):
                platform[0] += '、' + platform[i]
            type = response.xpath(u'//span[./text()="游戏类型: "]/following::text()[1]').extract()
            develop = response.xpath(u'//span[./text()="开发: "]/following::text()[1]').extract()
            all = [namechs, nameor, cat, date, star, rank, votes, platform, type, develop, img]
            allkey = ['namechs', 'nameor', 'cat', 'date', 'star', 'rank', 'votes', 'platform',
                      'type', 'develop', 'img']
        elif sub_cat == 'real':
            eps = response.xpath(u'//span[./text()="集数: "]/following::text()[1]').extract()
            date = response.xpath(u'//span[./text()="开始: "]/following::text()[1]').extract()
            director = response.xpath(u'//span[./text()="导演: "]/following::text()[1]').extract()
            author = response.xpath(u'//span[./text()="编剧: "]/following::text()[1]').extract()
            actor = response.xpath(u'//span[./text()="主演: "]/following::text()[1]').extract()
            country = response.xpath(u'//span[./text()="国家/地区: "]/following::text()[1]').extract()
            all = [namechs, nameor, cat, eps, date, star, rank, votes, director, author, actor, country, img]
            allkey = ['namechs', 'nameor', 'cat', 'eps', 'date', 'star', 'rank', 'votes', 'director', 'author',
                      'actor', 'country', 'img']

        cur = collections.OrderedDict()
        cur['id'] = int(id)
        cur['sub_cat'] = sub_cat
        for i in range(0, len(all)):
            if len(all[i]) >= 1:
                cur[allkey[i]] = all[i][0].strip('\r\n').strip('\n').replace('\r\n', ' ').replace('\n', ' ').replace(
                    '\\', '\\\\').replace('"', '\\"')
            else:
                cur[allkey[i]] = ''
        if len(tag) > 0:
            for i in range(0, len(tag)):
                tag[i] = tag[i].replace('\\', '\\\\').replace('"', '\\"')
            cur['tag'] = tag
        else:
            cur['tag'] = []

        ss = json.dumps(cur, ensure_ascii=False)
        self.f.write(str(str(ss)) + '\n')
        if int(id) % 100 == 0:
            self.f.flush()
