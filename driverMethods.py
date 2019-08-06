from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from platform import system
import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver.common.by import By


def create_driver(with_data=True):
    chrome_options = Options()
    chrome_options.add_argument('--always-authorized-plugins=true')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_extension('uBlock-Origin_v1.20.0.crx')
    if with_data:
        chrome_options.add_argument("--user-data-dir=chrome-data")
    if system().lower() == 'darwin':
        driver = webdriver.Chrome('chromedriver', options=chrome_options)
    else:
        driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    return driver


def login_to_youtube(driver, creds=None):
    if not creds:
        file = open(".creds2", "r")
        creds = file.read().splitlines()

    driver.get(
        'https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F'
        '%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3D%252F&hl=en'
        '&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    assert 'YouTube' in driver.title
    youtube_user = WebDriverWait(driver, 200).until(
        ec.visibility_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
    youtube_user.send_keys(creds[0] + '\n')

    youtube_pass = WebDriverWait(driver, 200).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="password'
                                                                                                '"]/div[1]/div/div['
                                                                                                '1]/input')))
    youtube_pass.send_keys(creds[1] + '\n')

    WebDriverWait(driver, 200).until(lambda x: x.find_element_by_xpath('//*[@id="search"]'))


def login_to_discord(driver, creds=None):
    if not creds:
        file = open(".creds2", "r")
        creds = file.read().splitlines()
    driver.get('http://discordapp.com/login')

    discord_user = WebDriverWait(driver, 200).until(
        ec.visibility_of_element_located(
            (By.XPATH, '//*[@id="app-mount"]/div[1]/div/div[2]/div/form/div/div[3]/div[1]/div/input')))
    discord_user.send_keys(creds[0])

    discord_pass = WebDriverWait(driver, 200).until(ec.visibility_of_element_located((By.XPATH,
                                                                                      '//*[@id="app-mount"]/div[1]/div/div[2]/div/form/div/div[3]/div[2]/div/input')))
    discord_pass.send_keys(creds[1] + '\n')


if __name__ == '__main__':
    login_to_discord(create_driver(False))
