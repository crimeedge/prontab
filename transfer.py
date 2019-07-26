from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from time import sleep

import pickle

if __name__ == '__main__':

    chrome_options = Options()
    chrome_options.add_argument('--always-authorized-plugins=true')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_extension('uBlock-Origin_v1.20.0.crx')
    chrome_options.add_argument("--user-data-dir=chrome-data")
    browser = webdriver.Chrome('chromedriver.exe',chrome_options=chrome_options)

    browser.get("https://transferring-videos.com/en/back/")