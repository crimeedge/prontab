from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


def create_driver(with_data=True):
    chrome_options = Options()
    chrome_options.add_argument('--always-authorized-plugins=true')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_extension('uBlock-Origin_v1.20.0.crx')
    if with_data:
        chrome_options.add_argument("--user-data-dir=chrome-data")
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    return driver


def login_to_youtube(driver):
    file = open(".creds2", "r")
    creds = file.read().splitlines()

    driver.get(
        'https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F'
        '%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3D%252F&hl=en'
        '&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    assert 'YouTube' in driver.title
    youtube_user = driver.find_element_by_xpath('//*[@id="identifierId"]')
    youtube_user.send_keys(creds[0] + '\n')

    youtube_pass = WebDriverWait(driver, 10).until(
        lambda x: x.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input'))
    youtube_pass.send_keys(creds[1] + '\n')

    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="search"]'))
