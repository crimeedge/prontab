import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec
import json
from selenium.common.exceptions import TimeoutException

from driverMethods import create_driver, login_to_youtube
from youtube.youtubeMake import get_api_service
from removePrivates import get_video_ids, filter_private_playlist_items
from youtube.youtubePlaylistItems import get_playlist_items_from_id
from youtube.youtubePlaylists import get_playlist_ids_list

from concurrent.futures import ThreadPoolExecutor
from pyformance import MetricsRegistry

import time


def add_vids(vid_tuple_sublist):
    driver = create_driver(False)
    driver.maximize_window()
    login_to_youtube(driver)
    num_playlists = len(get_playlist_ids_list(get_api_service()))
    broken_vids = []
    for vid_tuple in vid_tuple_sublist:
        ms = time.time()
        driver.get("https://www.youtube.com/watch?v=" + vid_tuple[0])
        try:
            WebDriverWait(driver, 10).until(ec.element_to_be_clickable(
                (By.CSS_SELECTOR, ".style-scope:nth-child(4) > .yt-simple-endpoint > #button"))).click()

            for i in range(2, num_playlists + 1):
                play_name = WebDriverWait(driver, 10).until(ec.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     ".style-scope:nth-child(" + str(
                         i) + ") > #checkbox > #checkboxLabel > #checkbox-container #label")))

                if play_name.text == vid_tuple[1]:
                    print(play_name.text)
                    play_name.click()
                    break

            time.sleep(0.5)
            reg.histogram("succ_add").add(time.time() - ms)
            print(reg.dump_metrics())
        except TimeoutException as ex:
            print(ex)
            print("https://www.youtube.com/watch?v=" + vid_tuple[0] + " machine broke")
            broken_vids.append(vid_tuple[0])
            try:
                reg.counter("broken").inc()
            except:
                print("reg machine broke!!!")
    driver.quit()
    return broken_vids


def get_ids_from_playlist_ids(youtube, playlist_ids):
    ret_video_ids = []
    for playlist_id in playlist_ids:
        curr_video_ids = get_video_ids(
            filter_private_playlist_items(get_playlist_items_from_id(youtube, playlist_id), False))
        ret_video_ids.extend(curr_video_ids)
    return ret_video_ids


mgs = time.time()
reg = MetricsRegistry()


def make_new_playlist(driver, name,
                      url='https://www.youtube.com/channel/UCuQjQ-iqbHh-hIMrDwfYfYA/playlists?disable_polymer=true'):
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable(
        (By.CSS_SELECTOR, "#playlists-tab-create-playlist-widget > .yt-uix-button > .yt-uix-button-content"))).click()
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[starts-with(@id,"kbd-nav")]'))).send_keys(name)
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR,
                                                                "#playlists-tab-create-playlist-dialog "
                                                                ".yt-uix-button-primary > "
                                                                ".yt-uix-button-content"))).click()
    WebDriverWait(driver, 10).until(ec.title_contains(name))


def make_tuple_diffs() -> int:
    known_video_ids = set()
    known_video_ids = known_video_ids.union(set((json.load(open('dMyKnown.json', 'r'))['video_ids'])))
    known_video_ids = known_video_ids.union(set(json.load(open('dBroken.json', 'r'))))
    jsons_in_order = ['dHvidsMakeover.json', 'dPoop.json', 'dH0.json', 'dHvidsBuzzcut.json', 'dHvidsCharity.json',
                      'dVsh.json']

    unknown_ids_tuples = []
    for jason in jsons_in_order:
        jason_ids = json.load(open(jason, 'r'))['video_ids']
        print(len(jason_ids))
        news_ids = set(jason_ids).difference(known_video_ids)
        print(len(news_ids))
        unknown_ids_tuples.extend((news_id, jason) for news_id in news_ids)
        print(len(unknown_ids_tuples))
        known_video_ids = known_video_ids.union(set(jason_ids))
        print(len(known_video_ids))

    print(unknown_ids_tuples)
    json.dump(unknown_ids_tuples, open('dDiffs.json', 'w'))
    return len(unknown_ids_tuples)


def add_diffs(diff_filename='dDiffs.json'):
    unknown_ids_tuples = json.load(open(diff_filename, 'r'))
    if len(unknown_ids_tuples) >= 1:

        if len(sys.argv) >= 4:
            all_process_tuples = unknown_ids_tuples[int(sys.argv[2]):int(sys.argv[3])]
        else:
            all_process_tuples = unknown_ids_tuples
        split_uvi = []
        i = 0
        num_drivers = 1
        if len(sys.argv) >= 2:
            num_drivers = int(sys.argv[1])
        print(len(all_process_tuples))
        while i < len(all_process_tuples):
            j = min(i + len(all_process_tuples) // num_drivers + 1, len(all_process_tuples))
            split_uvi.append(all_process_tuples[i:j])
            i = j

        for split in split_uvi:
            print(len(split))

        broken_total = json.load(open("dBroken.json", 'r'))
        try:
            with ThreadPoolExecutor(max_workers=len(split_uvi)) as threader:
                for _ in threader.map(add_vids, split_uvi):
                    broken_total.extend(_)
        except:
            print(sys.exc_info()[0])

        broken_total = list(set(broken_total))

        with open('dBroken.json', 'w') as outfile:
            json.dump(broken_total, outfile)
        reg.histogram("total").add(time.time() - mgs)
        print(reg.dump_metrics())
        print("done")


if __name__ == "__main__":
    # driver = create_driver()
    # jsons_in_order = ['dHvidsMakeover.json', 'dPoop.json', 'dH0.json', 'dHvidsBuzzcut.json', 'dHvidsCharity.json',
    #                   'dVsh.json']
    # for jason in jsons_in_order:
    #     make_new_playlist(driver,jason)
    # make_tuple_diffs()
    add_diffs('dDiffs.json')
    # add_diffs('dUDiffs.json')
