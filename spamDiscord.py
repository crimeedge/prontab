import json
import pyperclip
import time
from platform import system

import selenium.webdriver.support.expected_conditions as ec
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from driverMethods import create_driver, login_to_discord


def discord_wipe(driver):
    type_field = WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, ".textArea-2Spzkt")))
    while type_field.text.strip() != "":
        # type_field = WebDriverWait(driver, 20).until(
        #     ec.presence_of_element_located((By.CSS_SELECTOR, ".textArea-2Spzkt")))
        # print("field not empty: \n", type_field.text.strip())
        s_enter = ActionChains(driver)
        s_enter.send_keys("\n")
        s_enter.perform()


def spam_discord(known_video_ids, url='https://discordapp.com/channels/570509358677360650/570509358677360652'):
    driver = create_driver(False)
    login_to_discord(driver)
    time.sleep(3)
    driver.get(url)
    paste_text = ""
    if system().lower() == 'darwin':
        i = 0
        for video_id in known_video_ids:

            if i % 5 == 0:
                discord_wipe(driver)

            paste_text = ("http://youtu.be/%s" % video_id)
            pasty = ActionChains(driver)

            pasty.send_keys(paste_text)
            pasty.key_down(Keys.SHIFT)
            pasty.key_down(Keys.ENTER)
            pasty.key_up(Keys.SHIFT)
            pasty.key_up(Keys.ENTER)
            pasty.perform()
            i += 1
        discord_wipe(driver)
    elif system().lower() == 'windows':
        i = 0
        discord_wipe(driver)
        for video_id in known_video_ids:
            # TODO: fix length to 5, test on windows
            # if len(paste_text) < 100:
            #     paste_text += ("http://youtu.be/%s\n" % id)
            # else:
            if i % 5 == 0 and i > 0:
                pyperclip.copy(paste_text)
                pasty = ActionChains(driver)
                # pasty.click(type_field)
                pasty.key_down(Keys.CONTROL)
                pasty.key_down('v')
                pasty.key_up(Keys.CONTROL)
                pasty.key_up('v')
                # pasty.send_keys(paste_text)
                pasty.perform()

                discord_wipe(driver)
                paste_text = ""

            paste_text += ("http://youtu.be/%s\n" % video_id)
            i += 1

        pyperclip.copy(paste_text)
        pasty = ActionChains(driver)
        # pasty.click(type_field)
        pasty.key_down(Keys.CONTROL)
        pasty.key_down('v')
        pasty.key_up(Keys.CONTROL)
        pasty.key_up('v')
        # pasty.send_keys(paste_text)
        pasty.perform()
        discord_wipe(driver)
    driver.quit()


if __name__ == '__main__':
    unknown_ids_tuples = json.load(open('dMyKnown.json', 'r'))['video_ids'][:8]
    spam_discord(unknown_ids_tuples)
