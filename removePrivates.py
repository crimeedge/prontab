# -*- coding: utf-8 -*-
import os

import google_auth_oauthlib
import googleapiclient.discovery
from googleapiclient.errors import HttpError

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec

scope = ["https://www.googleapis.com/auth/youtube"]


def get_authenticated_service(scopes=scope):
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "o.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = run_selenium(flow)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube


def run_selenium(flow, **kwargs):
    kwargs.setdefault('prompt', 'consent')

    flow.redirect_uri = flow._OOB_REDIRECT_URI

    auth_url, _ = flow.authorization_url(**kwargs)

    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--user-data-dir=chrome-data")
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    driver.get(auth_url)
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.ID, "profileIdentifier"))).click()
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.LINK_TEXT, "Advanced"))).click()
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.LINK_TEXT, "Go to prontab (unsafe)"))).click()
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, ".M9Bg4d .RveJvd"))).click()
    WebDriverWait(driver, 20).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, "#submit_approve_access .RveJvd"))).click()
    code = WebDriverWait(driver, 20).until(
        ec.presence_of_element_located((By.XPATH,
                                        '// *[ @ id = "view_container"] / div / div / div[2] / div / div / div / form '
                                        '/ span / section / div / span / div / div / div / textarea '
                                        ))).text
    driver.quit()
    # code = input(authorization_code_message)

    flow.fetch_token(code=code)

    return flow.credentials


def get_playlist_ids_list(youtube):
    request = youtube.playlists().list(
        part="contentDetails",
        maxResults=50,
        mine=True
    )
    response = request.execute()
    return [item['id'] for item in response['items']]


def playlist_items(youtube, playlist_id="PLXoAM842ovaC5y2JmwjqNf9M4cosmGO12"):
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_id
    )
    items = []
    while request:
        response = request.execute()
        items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    return items

def filter_private_playlist_item_ids(items):
    privates = []
    for item in items:
        # print(item['snippet']['title'])
        if item['snippet']['title'] == 'Private video':
            privates.append(item['id'])
    return privates


def get_video_ids(items):
    video_ids = []
    for item in items:
        # print(item['snippet']['title'])
            video_ids.append(item['snippet']['resourceId']['videoId'])
    return video_ids


def delete_by_playlist_item_id(youtube, playlist_item_id):
    print ("del33ting playlistItem %s", playlist_item_id)
    request = youtube.playlistItems().delete(
        id=playlist_item_id
    )
    response = request.execute()
    return response


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = get_authenticated_service(scope)
    playlist_ids = get_playlist_ids_list(youtube)
    count = 0
    for playlist_id in playlist_ids:
        items = playlist_items(youtube, playlist_id)
        privates = filter_private_playlist_item_ids(items)
        for playlist_item_id in privates:
            try:
                print(playlist_item_id)
                delete_by_playlist_item_id(youtube, playlist_item_id)
                count += 1
            except HttpError as err:
                print(err)
    print('number of videos del33ted: %s', count)


if __name__ == "__main__":
    main()
