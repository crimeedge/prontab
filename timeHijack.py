# -*- coding: utf-8 -*-
from googleapiclient.errors import HttpError
from selenium.webdriver.support.ui import WebDriverWait
import re,time

from driverMethods import create_driver
from makeYoutube import get_api_service

video_id_prog = re.compile(r'v=([^&]+)')
time_prog = re.compile(r'&t=([^&]+)')
comment_prog = re.compile(r'(\d)+:(\d\d)')


def get_comment_time(youtube, video_id="MLVcmQ62luE", comment_author="Undesirable Truism"):
    request = youtube.commentThreads().list(
        part="snippet",
        searchTerms=comment_author,
        videoId=video_id
    )
    response = request.execute()
    for item in response['items']:
        if item['snippet']['topLevelComment']['snippet']['authorDisplayName'] == comment_author:
            comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
            min_sec = comment_prog.search(comment)
            if min_sec:
                return min_sec.group(1), min_sec.group(2)

    return None


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
    video_id = "INIT"
    # for _ in range(5):
    #     print(driver.current_url)
    #     time.sleep(5)
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
