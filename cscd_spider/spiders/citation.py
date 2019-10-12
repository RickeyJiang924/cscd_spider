# -*- coding: utf-8 -*-
import scrapy
import re
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class CitationSpider(scrapy.Spider):
    name = 'citation'
    fake_ua = UserAgent()
    headers = {"User-Agent": fake_ua.random, "Referer": "http://kns.cnki.net"}
    title = ""
    author = ""
    abstract = ""
    keywords = ""
    # allowed_domains = ['cnki.net']

    def start_requests(self):
        f = open("./selenium_test/href1.txt")
        start_urls = [item.strip("\n") for item in f.readlines()]
        for url in start_urls:
            try:
                yield scrapy.Request(url, headers=self.headers, dont_filter=True)
            except Exception:
                print("invalid request")
                break

    # def handle_problem(self):
    #     print("something wrong")

    def parse(self, response):
        # 获取标题
        self.title = response.xpath("//div[@class='wxTitle']/h2[@class='title']/text()").extract_first()

        # 获取作者
        author_array = []
        for span in response.xpath("//div[@class='author']/span"):
            author_array.append(span.xpath(".//a/text()").extract_first())
        self.author = ",".join(map(lambda x: str(x), author_array))

        # 获取摘要
        self.abstract = response.xpath("//span[@id='ChDivSummary']/text()").extract_first()

        # 获取关键词
        # 兄弟节点
        keywords_label = response.xpath("//label[@id='catalog_KEYWORD']/following-sibling::a/text()")
        for item in keywords_label.extract():
            self.keywords += str(item).strip(" ").strip("\n").strip("\r").strip(";").strip("“").strip("”")
            self.keywords += ","
        self.keywords.strip(",")

        # 引文在 #document 也就是新的页面 所以需要打开新的页面
        wxmain = response.xpath("/div[@class='wxmain']")
        citation_detail_url = wxmain.css('frame[id="frame1"]::attr(src)').extract_first()
        print(citation_detail_url)

        scrapy.Request(citation_detail_url, self.citation_detail_parse,
                       headers=self.headers, dont_filter=True)
        # yield {"title": title, "author": author, "abstract": abstract, "keywords": keywords, "citation": citation}

    # 获取引文
    def citation_detail_parse(self, response):
        citation = ""

        for div in response.xpath("//div[@class='essayBox']"):
            db_title = div.xpath(".//div[@class='dbTitle']/text()").text
            if re.match("中国图书全文数据库", db_title) is not None:
                continue
            for divv in div.xpath(".//a[@target='kcmstarget']/text()"):
                citation += divv
                citation += ","
        citation = citation.strip(",")
        yield {"title": self.title, "author": self.author, "abstract": self.abstract, "keywords": self.keywords, "citation": self.citation}


if __name__ == "__main__":
    print("爬虫有毒！！！")