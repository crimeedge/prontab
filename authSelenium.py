import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__=='__main__':
    chrome_options = Options()
    chrome_options.add_argument('--always-authorized-plugins=true')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--user-data-dir=chrome-data")
    driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("user-data-dir=chrome-data")
    driver.get('https://google.com')
    time.sleep(30)  # Time to enter credentials
    driver.quit()