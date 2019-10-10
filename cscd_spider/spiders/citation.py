# -*- coding: utf-8 -*-
import scrapy
import re


class CitationSpider(scrapy.Spider):
    name = 'citation'
    headers = {
        "Host": "ref.cnki.net",
        "Accept": "text/css,*/*;q=0.1",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://ref.cnki.net/REF/AdvSearch",  # "http://lib.imut.edu.cn/info/1006/4042.htm",
        "Cookie": "Ecp_ClientId=3181004223202368812; cnkiUserKey=b4f8eab1-9b2e-acd3-f303-05e74814c183; UM_distinctid=16a4a3b4fad3d8-0376ab6c52e634-11656d4a-1fa400-16a4a3b4fae703; ASP.NET_SessionId=sy5su2sch4pi1yfhugt0v4vj; LID=WEEvREcwSlJHSldRa1Fhb09jT0lPd2FQSGN0UFR2YklQelFEbkhlYTFNND0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; SID_ref=203103; SID_refport=203102; Ecp_session=1; Ecp_IpLoginFail=191009180.111.26.86; SID=203103",
        "Connection": "keep-alive"
    }
    # allowed_domains = ['cnki.net']
    # start_urls = ['http://cnki.net/']

    def start_requests(self):
        response = scrapy.Request("http://ref.cnki.net/REF/AdvSearch",
                                  headers=self.headers, callback=self.handle_problem(),
                                  dont_filter=True)
        yield response

    def handle_problem(self):
        print("something wrong")

    def parse(self, response):
        content_urls = []
        # print(response.body)
        for tr in response.xpath('//table[@class="elist"]'):
            # self.log(li.extract())
            url = tr.xpath(".//a[@class='title']/a/@href").extract_first()
            content_urls.append(url)
            # title_href = li.xpath(".//a[@class='truetit']/@href").extract_first()
            # url = "https://bbs.hupu.com" + title_href
            # post_id = self.get_post_id(title_href)
            # title = li.xpath(".//a[@class='truetit']/text()").extract_first()
            # author = li.xpath(".//a[@class='aulink']/text()").extract_first()
            # post_time = li.xpath(".//a[@style='color:#808080;cursor: initial; ']/text()").extract_first()
            # count_des = li.xpath(".//span[@class='ansour box']/text()").extract_first()
            # reply_count = re.match('(\d+)[^0-9]*(\d+)', count_des).group(1)
            # view_count = re.match('(\d+)[^0-9]*(\d+)', count_des).group(2)
            # content_urls.append(url)
            #
            # yield {"id": post_id, "title": title, "url": url, "author": author, "post_time": post_time,
            #        "view_count": view_count, "reply_count": reply_count}
        print(content_urls)
        for content_url in content_urls:
            yield scrapy.Request(content_url, self.detail_parse, dont_filter=True)

    def detail_parse(self, response):
        # 获取标题
        title = response.xpath("//div[@class='wxTitle']/h2[@class='title']/text()").extract_first()

        # 获取作者
        author_array = []
        for span in response.xpath("//div[@class='author']/span"):
            author_array.append(span.xpath(".//a/text()").extract_first())
        author = ",".join(map(lambda x: str(x), author_array))

        # 获取引文
        citation_array = []
        for div in response.xpath("//div[@class='essayBox']"):
            db_title = div.xpath(".//div[@class='dbTitle']/text()").extract_first()
            if re.match("中国图书全文数据库", db_title) is not None:
                for divv in div.xpath(".//a[@target='kcmstarget']/text()"):
                    citation_array.append(divv)
        citation = ",".join(map(lambda x: str(x), citation_array))
        yield {"title": title, "author": author, "citation": citation}


if __name__ == "__main__":
    '''content = window.location.href='https://bbs.hupu.com/'+url''\n
    hello
            }
          }
        }
       break;
     default:
       break;
   }

  }
},{
  pageCount:10,//总页码,默认10
  current:1,//当前页码
  name:detail_url+'-',//标记
  hname:detail_url,
  showNear:pageNum,//显示当前页码前多少页和后多少页，默认2
  pageSwap:true,
  align:'right',
  is_read:1,
  showSumNum:false,//是否显示总页码
  maxpage:10

    '''