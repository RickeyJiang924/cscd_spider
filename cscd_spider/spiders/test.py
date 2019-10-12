from lxml import etree
from urllib import request
import re
from selenium import webdriver
import time
import urllib.request
from selenium.webdriver.chrome.options import Options
from pyquery import PyQuery as pq


# req = request.urlopen('http://ref.cnki.net/REF/Redirect?url=%2Fkcms%2Fdetail%2Fdetail.aspx%3Fdbcode%3DCJFD%26dbname%3DCJFD2003%26filename%3DNKJJ200302000%26v%3DMDY2MThRS0RIODR2UjRUNmo1NE8zenFxQnRHRnJDVVJMT2VaK2R0RnkvbVVyek9LeWJCWkxHNEh0TE1yWTlGWkk%3D&type=1&ktype=Default')
#
# middle = etree.HTML(req.read())
#
# print(re.match("中国图书全文数据库", "sadasd"))
# m = middle.xpath("//label[@id='catalog_KEYWORD']/following-sibling::a/text()")
# for item in m:
#     print(str(item).strip(" ").strip("\n").strip("\r").strip(";").strip("“").strip("”"))
# wxmain = middle.xpath("//div[@class='wxmain']")
# for i in wxmain:
#     print(i.find("iframe").attrib)

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome("C:/Users/Andre\AppData\Local\Programs\Python\Python37\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe",
#                           options=chrome_options)
# driver.get("http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode=CJFD&filename=lzxk200502029&dbname=CJFD2005&RefType=1&vl=")
# citation = ""
# for div in driver.find_elements_by_xpath("//div[@class='essayBox']"):
#     db_title = div.find_element_by_xpath(".//div[@class='dbTitle']").text
#     if re.match("中国图书全文数据库", db_title) is not None:
#         continue
#     for divv in div.find_elements_by_xpath(".//a[@target='kcmstarget']"):
#         citation += divv.text
#         citation += ","
# print(str(citation).strip(","))
# iframe = driver.find_elements_by_tag_name('iframe')[0]
# driver.switch_to.frame(iframe)
# print(driver.page_source)
doc = pq(url="http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&dbname=CJFD2005&filename=LZXK200502029&v=MjUyMDBLVGZUWmJHNEh0VE1yWTlIYllRS0RIODR2UjRUNmo1NE8zenFxQnRHRnJDVVJMT2VaK2R0RnkvbVVyek8=&uid=")
print(doc)
result = doc('#frame1')
# http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&dbname=CJFD2005&filename=LZXK200502029&v=MjUyMDBLVGZUWmJHNEh0VE1yWTlIYllRS0RIODR2UjRUNmo1NE8zenFxQnRHRnJDVVJMT2VaK2R0RnkvbVVyek8=&uid=
# http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode=CJFD&filename=lzxk200502029&dbname=CJFD2005&RefType=1&vl=

