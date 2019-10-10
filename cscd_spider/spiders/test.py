from selenium import webdriver
import time

chrome_driver = "C:/Users/Andre/AppData\Local\Programs\Python\Python37\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
browser = webdriver.Chrome(executable_path=chrome_driver)
time.sleep(5)
