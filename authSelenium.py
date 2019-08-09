import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def auth_selenium(url='https://youtube.com'):
    print(sys.argv)
    chrome_options = Options()
    chrome_options.add_argument('--always-authorized-plugins=true')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--user-data-dir=chrome-data")
    chrome_options.add_extension('uBlock-Origin_v1.20.0.crx')
    chrome_options.add_argument("user-data-dir=chrome-data")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(60)  # Time to enter credentials
    driver.quit()


if __name__ == '__main__':
    auth_selenium("https://hvids.net")
