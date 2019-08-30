import json
from typing import List

import pyperclip
import time
from platform import system

import selenium.webdriver.support.expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from driverMethods import create_driver, login_to_discord
from youtube.youtubeMake import get_api_service
from youtube.youtubeVideos import _get_parts_from_video_ids


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


def prepare_discord(driver, url):
    time.sleep(3)
    driver.get(url)
    try:
        WebDriverWait(driver, 1).until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".lookFilled-1Gx00P"))).click()
    except TimeoutException:
        print("click on cont timeout")


def paste_discord(driver, known_video_ids):
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
        clipboard_storage = pyperclip.paste()
        i = 0
        discord_wipe(driver)
        for video_id in known_video_ids:
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
        pyperclip.copy(clipboard_storage)


def spam_discord(driver, known_video_ids, url='https://discordapp.com/channels/570509358677360650/570509358677360652'):
    prepare_discord(driver, url)
    paste_discord(driver, known_video_ids)
    # hard coded sleep
    time.sleep(len(known_video_ids) / 5.0)
    driver.quit()


def filter_polish_from_vid_list(youtube, ids: List[str], driver):
    print(len(ids))
    # filtereds = []
    i = 0
    while i < len(ids):
        j = min(i + 50, len(ids))
        for item in _get_parts_from_video_ids(youtube, ids[i:j], "snippet")['items']:
            if "Ś" in item['snippet']['title'] or "Ł" in item['snippet']['title']:
                paste_discord(driver, [item['id']])
        i = j
    # print(len(filtereds))
    # return filtereds


if __name__ == '__main__':
    unknown_ids_tuples = json.load(open('dMyKnown.json', 'r'))['video_ids']
    driver = create_driver(True,False)
    prepare_discord(driver,'https://discordapp.com/channels/464754024802025487/466070782439718922')
    filter_polish_from_vid_list(get_api_service(),unknown_ids_tuples,driver)