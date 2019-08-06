from collections import deque

import googleapiclient

from getUnlisted import get_unlisteds_from_list
from removePrivates import get_playlist_ids_list, get_playlist_items_from_id, get_video_ids
from makeYoutube import get_authenticated_service, get_api_service

import json


def my_youtube_ids_to_json():
    youtube = get_api_service()

    playlist_ids = get_playlist_ids_list(youtube)

    known_video_ids = []

    for playlist_id in playlist_ids:
        items = get_playlist_items_from_id(youtube, playlist_id)
        known_video_ids.extend(get_video_ids(items))
    broken_total = json.load(open("dataBroken.json", 'r'))
    print(len(broken_total))
    print(len(known_video_ids))
    known_video_ids.extend(broken_total)
    known_video_ids = list(set(known_video_ids))
    print(len(known_video_ids))
    with open('dataKnown.json', 'w') as outfile:
        json.dump(known_video_ids, outfile)


def other_youtube_ids_to_json():
    youtube = get_api_service()
    # h0 liked, poop liked
    playlist_ids = ['LLhNOMudRAcLnj6hlCLjLk9A', 'LLzjiyMpyPuHnQyVFp9Nimbg']
    # h0 channel
    playlist_ids.extend(get_playlist_ids_list(youtube, "UChNOMudRAcLnj6hlCLjLk9A"))
    # poop channel
    playlist_ids.extend(get_playlist_ids_list(youtube, 'UCzjiyMpyPuHnQyVFp9Nimbg'))

    known_video_ids = []

    for playlist_id in playlist_ids:
        items = get_playlist_items_from_id(youtube, playlist_id)
        known_video_ids.extend(get_video_ids(items))
    known_video_ids = list(set(known_video_ids))
    print(len(known_video_ids))
    with open('dataH0Poop.json', 'w') as outfile:
        json.dump(known_video_ids, outfile)

def store_differences_to_json():
    diffs = set(json.load(open('dataH0Poop.json', 'r'))).difference(set(json.load(open('dataKnown.json', 'r'))))
    print (len(diffs))
    with open('dataDiffs.json', 'w') as outfile:
        json.dump(list(diffs), outfile)

def temp_unlisted():
    youtube = get_api_service()
    playlist_ids = ['PLXoAM842ovaAO2MHT2ZyED3Gs5Ifmdm1G']

    known_video_ids = []

    for playlist_id in playlist_ids:
        items = get_playlist_items_from_id(youtube, playlist_id)
        known_video_ids.extend(get_video_ids(items))
    known_video_ids = list(set(known_video_ids))
    print(len(known_video_ids))
    print(get_unlisteds_from_list(youtube,known_video_ids,True))
    with open('dataTempUnlisted.json', 'w') as outfile:
        json.dump(known_video_ids, outfile)

if __name__ == "__main__":
    # my_youtube_ids_to_json()
    # other_youtube_ids_to_json()
    # store_differences_to_json()
    temp_unlisted()
