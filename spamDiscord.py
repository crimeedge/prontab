import json, pyperclip, time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec
from platform import system

from driverMethods import create_driver, login_to_discord

if __name__ == '__main__':
    driver = create_driver(False)
    login_to_discord(driver)
    time.sleep(3)
    driver.get('https://discordapp.com/channels/570509358677360650/570509358677360652')
    known_video_ids = json.load(open('dataUnlisted.json', 'r'))
    paste_text = ""
    for id in known_video_ids:
        if len(paste_text) < 1980:
            paste_text += ("http://youtu.be/%s\n" % id)
        else:
            # print(paste_text)
            # raise ZeroDivisionError
            pyperclip.copy(paste_text)
            pasty = ActionChains(driver)
            type_field = WebDriverWait(driver,20).until(ec.presence_of_element_located ((By.CSS_SELECTOR, ".textArea-2Spzkt")))
            pasty.click(type_field)
            # pasty.key_down(Keys.COMMAND)
            # pasty.key_down('v')
            # pasty.key_up(Keys.COMMAND)
            # pasty.key_up('v')
            pasty.send_keys(paste_text)
            # pasty.send_keys(Keys.ENTER)
            pasty.perform()
            paste_text = ("http://youtu.be/%s\n" % id)


