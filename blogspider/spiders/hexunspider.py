# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request

from blogspider.items import BlogspiderItem
from scrapy.http import Request


class HexunspiderSpider(scrapy.Spider):
    name = 'hexunspider'
    allowed_domains = ['hexun.com']
    # start_urls = ['http://hexun.com/']
    user_id = "19940007"

    def start_requests(self):
        url = "http://" + str(self.user_id) + ".blog.hexun.com/p1/default.html"
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
        yield Request(url, headers=headers)

    def parse(self, response):
        item = BlogspiderItem()
        item['name'] = response.xpath('//span[@class="ArticleTitleText"]/a/text()').extract()
        item['url'] = response.xpath('//span[@class="ArticleTitleText"]/a/@href').extract()

        item['hits'], item['comment'] = self.get_click_comment_count(response)

        yield item

        total_page_count = int(self.get_total_page(response))
        if total_page_count > 1:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
            for i in range(2, total_page_count + 1):
                nexturl = "http://" + str(self.user_id) + ".blog.hexun.com/p" + str(i) + "/default.html"
                yield Request(nexturl, callback=self.parse, headers=headers)

    def get_total_page(self, response):
        """
        获取总页数
        :param response:
        :return:
        """
        page_number_pattern = 'blog.hexun.com/p(.*?)/default.html'
        page_number = re.findall(page_number_pattern, str(response.body))
        if len(page_number) > 1:
            return page_number[-2]
        else:
            return 1

    def get_click_comment_count(self, response):
        """
        获取点击与评论数
        :param response:
        :return:
        """
        self.set_headers()

        target_pattern = '<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'
        hurl = re.findall(target_pattern, str(response.body))[0]
        target_html = urllib.request.urlopen(hurl).read()
        target_html = str(target_html)

        hits_pattern = "click\d*?','(\d*?)'"
        comment_pattern = "comment\d*?','(\d*?)'"
        hits_list = re.findall(hits_pattern, target_html)
        comment_list = re.findall(comment_pattern, target_html)

        return hits_list, comment_list

    def set_headers(self):
        """
        模拟成浏览器
        :return:
        """
        headers2 = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers2]
        urllib.request.install_opener(opener)


"""
create table blogdata(id int(10) auto_increment primary key not null,name varchar(30),url varchar(100),hits int(15),comment int(15));
"""
