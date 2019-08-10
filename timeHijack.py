# -*- coding: utf-8 -*-
from googleapiclient.errors import HttpError
from selenium.webdriver.support.ui import WebDriverWait
import re

from driverMethods import create_driver
from progs import video_id_prog, time_prog
from youtube.youtubeComments import get_comment_time
from youtube.youtubeMake import get_api_service

video_id = "INIT"


def check_diff_video_id(driver):
    # global driver
    global video_id
    vee = video_id_prog.search(driver.current_url)
    if vee:
        if not video_id == vee.group(1):
            return True
    return False


def main():
    youtube = get_api_service()
    # global driver
    driver = create_driver()
    driver.get("https://www.youtube.com")
    global video_id

    for _ in range(99999):
        WebDriverWait(driver, 99999).until(check_diff_video_id)
        video_id = video_id_prog.search(driver.current_url).group(1)
        print(video_id)
        try:
            ms_pair = get_comment_time(youtube, video_id)
        except HttpError as err:
            print(err)
            ms_pair = None
        if ms_pair:
            hijacked_link = re.sub(time_prog, "", driver.current_url) + '&t=' + ms_pair[0] + 'm' + ms_pair[1] + 's'
            print(hijacked_link)
            driver.get(hijacked_link)
    # print(get_comment_time(youtube))


if __name__ == "__main__":
    main()
