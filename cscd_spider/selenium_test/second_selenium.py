from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
import pymysql


def pre_process_request():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(
        "C:/Users/Andre\AppData\Local\Programs\Python\Python37\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe",
        options=chrome_options)
    count = 0
    f = open("href1.txt")
    href = [i.strip("\n") for i in f.readlines()]
    count += process_request(driver, href)
    f = open("href2.txt")
    href = [i.strip("\n") for i in f.readlines()]
    count += process_request(driver, href)
    print(count)


def process_request(driver, href):
    # # 打开数据库连接
    # db = pymysql.connect("localhost", "root", "jrq.l.iggy09", "cscd")
    # # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    count = 0
    for i in href:
        try:
            driver.get(i.strip("\n").strip())
            # 获取标题
            title = driver.find_element_by_xpath("//div[@class='wxTitle']/h2[@class='title']").text
            # 获取作者
            author_array = []
            for span in driver.find_elements_by_xpath("//div[@class='author']/span"):
                author_array.append(span.text)
            author = ",".join(map(lambda x: str(x), author_array))

            # 获取摘要
            abstract = driver.find_element_by_xpath("//span[@id='ChDivSummary']").text
            abstract = str(abstract.strip())

            # 获取关键词
            # 兄弟节点
            keywords = ""
            keywords_label = driver.find_elements_by_xpath("//label[@id='catalog_KEYWORD']/following-sibling::a")
            for item in keywords_label:
                keywords += str(item.text).strip(" ").strip("\n").strip("\r").strip(";").strip("“").strip("”")
                keywords += ","
            keywords = keywords.strip(",")

            # 引文在 #document 也就是新的页面
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # time.sleep(1)
            iframe = driver.find_elements_by_id("frame1")[0]
            driver.switch_to.frame(iframe)
            citation = ""
            for div in driver.find_elements_by_xpath("//div[@class='essayBox']"):
                db_title = div.find_element_by_xpath(".//div[@class='dbTitle']").text
                if re.match("中国图书全文数据库", db_title) is not None:
                    continue
                for divv in div.find_elements_by_xpath(".//a[@target='kcmstarget']"):
                    citation += divv.text
                    citation += ","
            citation = citation.strip(",")
            # print(title + "\n" + author + "\n" + abstract + "\n" + keywords + "\n" + citation)
            # 使用三引号防止出现转义错误
            # insert_sql = '''
            #     insert into paper(title,author,abstract,keywords,citation) values (%s,%s,%s,%s,%s)
            # '''
            # cursor.execute(insert_sql, (title, author, abstract, keywords, citation))
            txt = open("information.txt", "a+")
            txt.write(title + "\n")
            txt.write(author + "\n")
            txt.write(abstract + "\n")
            txt.write(keywords + "\n")
            txt.write(citation + "\n\n")
            count += 1
            print(str(count) + " " + title)
        except Exception:
            continue
        # db.commit()
    return count
    # db.close()


if __name__ == "__main__":
    pre_process_request()
