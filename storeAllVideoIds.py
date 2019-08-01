from collections import deque

import googleapiclient

from removePrivates import get_playlist_ids_list, playlist_items, get_video_ids, get_authenticated_service

import json

if __name__ == "__main__":
    api_service_name = "youtube"
    api_version = "v3"
    key = open('.creds').readlines()[0].strip()

    youtube = get_authenticated_service()

    playlist_ids = get_playlist_ids_list(youtube)

    known_video_ids = []

    for playlist_id in playlist_ids:
        if not playlist_id == 'PLXoAM842ovaDEU76pkObKtgYjNE9rWiUc':
            items = playlist_items(youtube, playlist_id)
            known_video_ids.extend(get_video_ids(items))

    print(len(known_video_ids))
    with open('dataNoApi.txt', 'w') as outfile:
        json.dump(known_video_ids, outfile)