from collections import deque

import googleapiclient

from removePrivates import get_playlist_ids_list, get_playlist_items_from_id, get_video_ids
from makeYoutube import get_authenticated_service, get_api_service

import json

if __name__ == "__main__":

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
