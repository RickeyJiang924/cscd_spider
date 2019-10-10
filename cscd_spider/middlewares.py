# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
import time


class ClickMiddleware(object):
    # 模拟鼠标点击，选中/不选中单选框
    def process_request(self, request, spider):
        click_page_url = "http://ref.cnki.net/REF/AdvSearch"
        if request.url == click_page_url:
            driver_address = "C:/Users/Andre\AppData\Local\Programs\Python\Python37\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
            driver = webdriver.Chrome(executable_path=driver_address)
            try:
                driver.get(request.url)
                # driver.implicitly_wait(3)
                time.sleep(3)

                # dissertation = "//input[@id='cb_beref_cdmd']"  # 学位论文
                dissertation = driver.find_element_by_id("cb_beref_cdmd")  # 学位论文

                # newspaper = "//input[@id='cb_beref_ccnd']"  # 报纸
                newspaper = driver.find_element_by_id("cb_beref_ccnd")  # 报纸

                # magazine = "//input[@id='cb_beref_cbbd']"  # 图书
                magazine = driver.find_element_by_id("cb_beref_cbbd")  # 图书

                # foreign = "//input[@id='cb_beref_crldeng']"  # 外文
                foreign = driver.find_element_by_id("cb_beref_crldeng")  # 外文

                # others = "//input[@id='cb_beref_wfb']"  # 其他
                others = driver.find_element_by_id("cb_beref_wfb")  # 其他

                no_need = [dissertation, newspaper, magazine, foreign, others]
                for item in no_need:
                    # 数据由js来控制,点击后加载数据
                    item.click()
                    # driver.find_element_by_xpath(item).click()
                    # time.sleep(5)

                # 默认为检索主题
                theme_text = driver.find_element_by_id("article_1_value_1")
                theme_text.send_keys("经济学")

                # 按下“搜索”按钮
                search_button = driver.find_element_by_id("advSearchBtn")
                search_button.click()

                true_page = driver.page_source
                time.sleep(3)
                driver.close()

                return HtmlResponse(request.url, body=true_page, encoding='utf-8', request=request)

            except BaseException:
                print("get news data failed")
        else:
            return None


# class CscdSpiderSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
#
#
# class CscdSpiderDownloaderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)

