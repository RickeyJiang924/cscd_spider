from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import urllib.request
from PIL import Image, ImageEnhance
from selenium.webdriver.chrome.options import Options
import pytesser3


def pre_process_request(url):
    click_page_url = url
    driver_address = "C:/Users/Andre\AppData\Local\Programs\Python\Python37\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(executable_path=driver_address, options=chrome_options)
    driver = webdriver.Chrome(executable_path=driver_address)
    driver.maximize_window()

    driver.get(click_page_url)
    # driver.implicitly_wait(3)
    time.sleep(1)

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

    time.sleep(1)  # 4191
    for i in range(4190):
        next_page = driver.find_element_by_class_name("next")
        next_page.click()
    process_request(driver)


def process_request(driver):
    next_page = ""
    while next_page is not None:
        try:
            driver.find_element_by_xpath("//table[@class='elist']")
        # 有验证码出现的情况
        except Exception:
            # 自动识别
            try:
                while driver.find_element_by_id("changeVercode") is not None:
                    time.sleep(3)
                    image_item = driver.find_element_by_id("changeVercode")
                    image_item.click()
                    image_item.screenshot("check_picture/checkbox2.png")
                    # driver.save_screenshot("check_picture/checkbox2.png")
                    # left = image_item.location["x"]
                    # top = image_item.location["y"]
                    # right = image_item.location["x"] + image_item.size["width"]
                    # bottom = image_item.location["y"] + image_item.size["height"]

                    # 识别验证码
                    # code = verify_code_by_url(image_item.get_attribute("src"),
                    # "check_picture/checkbox1.jpg")  # 从链接获取图片
                    code = verify_code_by_screenshot("check_picture/checkbox2.png")  # 截图获取图片

                    # 填充验证码
                    driver.find_element_by_id("vericode").click()
                    driver.find_element_by_id("vericode").clear()
                    driver.find_element_by_id("vericode").send_keys(code)

                    # 点击提交按钮
                    driver.find_element_by_id("checkCodeBtn").click()

                # 人工识别
                # 输入中断
                # input()
            except Exception:
                return process_request(driver)
            return process_request(driver)

        # 正常爬取
        try:
            time.sleep(2)
            file = open("href1.txt", "a+")
            next_page = driver.find_element_by_class_name("next")
            for url in driver.find_elements_by_xpath('//div[@class="listCont"]//a[@class="title"]'):
                # print(url.get_attribute("href"))
                file.write(url.get_attribute("href"))
                file.write('\n')
            file.close()
            next_page.click()
        except Exception:
            return process_request(driver)

    driver.close()


def verify_code_by_screenshot(image_address):
    # image = Image.open(image_address)
    # image = image.crop((left, top, right, bottom))
    # image.save(image_address)
    return verify_code(image_address)


def verify_code_by_url(image_url, image_address):
    urllib.request.urlretrieve(image_url, image_address)
    return verify_code(image_address)


def verify_code(image_address):
    image = Image.open(image_address)
    # 转为灰度图像 设定二值化阈值
    image = image.convert('L')
    # 对比度增强
    sharpness = ImageEnhance.Contrast(image)
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save(image_address)
    result = pytesser3.image_file_to_string(image_address).replace(" ", "")
    result.replace("/", "1")
    result.replace("\\N", "W")
    # result.replace("(", "C")
    print(result)
    return result


if __name__ == "__main__":
    pre_process_request("http://ref.cnki.net/REF/AdvSearch")
    # verify_code("http://ref.cnki.net/REF/Common/VerifyCode?t=0.3285117217251785")
