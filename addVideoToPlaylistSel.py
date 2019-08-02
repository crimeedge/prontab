from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec
import re
import sys
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.common.exceptions import TimeoutException

from driverMethods import create_driver, login_to_youtube
from makeYoutube import get_authenticated_service, get_api_service
from removePrivates import get_video_ids, get_playlist_items_from_id, filter_private_playlist_items

video_id_prog = re.compile(r'v=([^&]+)')
index_prog = re.compile(r'index=5\d\d\d')


# def load_test(driver):
#     driver.get('https://www.youtube.com/playlist?list=LLhNOMudRAcLnj6hlCLjLk9A&disable_polymer=true')
#     for i in range(1, 5001):
#         # WebDriverWait(driver, 20).until(
#         #     ec.presence_of_element_located((By.XPATH, '//*[@id="masthead-search-term"]'))).click()
#         # actions = ActionChains(driver)
#         # actions.move_to_element_with_offset(WebDriverWait(driver, 20).until(
#         #     ec.presence_of_element_located((By.XPATH, '//*[@id="masthead-search-term"]'))), 15, 100)
#         # actions.click()
#         # actions.perform()
#
#         # element = WebDriverWait(driver, 3).until(
#         #     ec.presence_of_element_located((By.XPATH,
#         #                                     '// *[ @ id = "pl-load-more-destination"] / tr[' + str(
#         #                                         i) + '] / td[3] / span / button[1]')))
#
#         element = driver.find_element(By.XPATH,
#                                       '//*[@id="pl-video-list"]/button/span/span[2]')
#         actions = ActionChains(driver)
#         actions.move_to_element(element).perform()
#
#         element = driver.find_element(By.XPATH,
#                                       '// *[ @ id = "pl-load-more-destination"] / tr[' + str(
#                                           i) + '] / td[3] / span / button[1]')
#         actions = ActionChains(driver)
#         actions.move_to_element(element).perform()
#         WebDriverWait(driver, 3).until(
#             ec.element_to_be_clickable((By.XPATH, '// *[ @ id = "pl-load-more-destination"] / tr[' + str(
#                 i) + '] / td[3] / span / button[1]'))).click()
#
#         if i % 100 == 0:
#             WebDriverWait(driver, 20).until(
#                 ec.element_to_be_clickable((By.XPATH, '//*[@id="pl-video-list"]/button/span/span[2]'))).click()
#
#         # // *[ @ id = "pl-load-more-destination"] / tr[1] / td[3] / span / a / span / span / span / img


# def scroll_test(driver):
#     driver.get('https://www.youtube.com/playlist?list=LLhNOMudRAcLnj6hlCLjLk9A')
#     SCROLL_PAUSE_TIME = 2
#     # time.sleep(5)
#     # Get scroll height
#     last_height = driver.execute_script("return document.documentElement.scrollHeight")
#     print(last_height)
#
#     for i in range(1, 2):
#         element = driver.find_element(By.CSS_SELECTOR,
#                                       ".style-scope:nth-child(" + str(i) + ")")
#         actions = ActionChains(driver)
#         actions.move_to_element(element).perform()
#         WebDriverWait(driver, 5).until(ec.element_to_be_clickable(
#             (By.CSS_SELECTOR, ".ytd-playlist-video-list-renderer:nth-child(" + str(
#                 i) + ") > #menu #button > #button > .style-scope"))).click()
#         WebDriverWait(driver, 5).until(ec.element_to_be_clickable(
#             (By.CSS_SELECTOR,
#              ".ytd-menu-popup-renderer:nth-child(1) > .style-scope > .style-scope:nth-child(2)"))).click()
#
#         # driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
#         # # Wait to load page
#         # time.sleep(SCROLL_PAUSE_TIME)
#         #
#         # # Calculate new scroll height and compare with last scroll height
#         # new_height = driver.execute_script("return document.documentElement.scrollHeight")
#         # if new_height == last_height:
#         #     break
#         # last_height = new_height
#         # print(last_height)
#     # driver.quit()


def next_test(driver):
    # url = "https://www.youtube.com/watch?v=1970HF7f2cE&list=LLhNOMudRAcLnj6hlCLjLk9A&index=1849"
    url = "https://www.youtube.com/watch?v=ILrhMTJofLw&list=LLhNOMudRAcLnj6hlCLjLk9A&index=3733"
    driver.get(url)
    i = 0
    already_seen = 0
    try:
        while i < 3151 and not index_prog.search(driver.current_url):
            url = driver.current_url
            if not video_id_prog.search(url).group(1) in known_video_ids:
                WebDriverWait(driver, 200).until(ec.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".style-scope:nth-child(4) > .yt-simple-endpoint > #button"))).click()
                WebDriverWait(driver, 200).until(ec.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     ".style-scope:nth-child(2) > #checkbox > #checkboxLabel > #checkbox-container #label"))).click()
            else:
                already_seen += 1
                print(url + " already in " + known_file + " " + str(already_seen))
            actions = ActionChains(driver)
            actions.key_down(Keys.SHIFT)
            actions.key_down('n')
            actions.key_up(Keys.SHIFT)
            actions.key_up('n')
            actions.perform()
            # WebDriverWait(driver, 20).until(ec.element_to_be_clickable(
            #     (By.CSS_SELECTOR, "#button > .ytd-add-to-playlist-renderer"))).click()
            # WebDriverWait(driver, 20).until(ec.element_to_be_clickable(
            #     (By.CSS_SELECTOR, ".ytp-next-button"))).click()
            WebDriverWait(driver, 200).until(lambda x: not driver.current_url == url)
            driver.get(driver.current_url)
            i += 1

    except TimeoutException as ex:
        print(ex)
        print(url)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print(url)
    print('scrape finish')


def dupe_test(driver):
    video_ids = get_video_ids(get_playlist_items_from_id(youtube, 'PLXoAM842ovaDEU76pkObKtgYjNE9rWiUc'))
    dupes = []
    for video_id in video_ids:
        if video_id in known_video_ids:
            dupes.append(video_id)
    print(len(dupes))
    for dupe in dupes:
        driver.get("https://www.youtube.com/watch?v=" + dupe)
        WebDriverWait(driver, 200).until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR, ".style-scope:nth-child(4) > .yt-simple-endpoint > #button"))).click()
        WebDriverWait(driver, 200).until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".style-scope:nth-child(2) > #checkbox > #checkboxLabel > #checkbox-container #label"))).click()
        # break


def add_vids(vid_sublist):
    driver = create_driver(False)
    driver.maximize_window()
    login_to_youtube(driver)
    for vid in vid_sublist:
        driver.get("https://www.youtube.com/watch?v=" + vid)
        WebDriverWait(driver, 200).until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR, ".style-scope:nth-child(4) > .yt-simple-endpoint > #button"))).click()
        WebDriverWait(driver, 200).until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR,
             ".style-scope:nth-child(2) > #checkbox > #checkboxLabel > #checkbox-container #label"))).click()


if __name__ == "__main__":

    known_file = 'data3373.txt'
    playlist_id = 'LLhNOMudRAcLnj6hlCLjLk9A'

    known_video_ids = []
    try:
        known_video_ids = json.load(open(known_file, 'r'))
    except FileNotFoundError as err:
        # print("Unexpected error:", sys.exc_info()[0])
        print(err)
        print("known_video_ids grab failure")
        raise SystemExit
    youtube = get_api_service()

    video_ids = get_video_ids(filter_private_playlist_items( get_playlist_items_from_id(youtube, playlist_id),False))

    unknown_video_ids = list(set(video_ids).difference(set(known_video_ids)))

    # driver = create_driver(False)
    #
    # driver.maximize_window()
    #
    # login_to_youtube(driver)
    # next_test(driver)
    # dupe_test(driver)
