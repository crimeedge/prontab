from typing import List

from getUnlisted import get_unlisteds_from_list, get_statuses_from_video_ids
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
    # broken_total = json.load(open("dBroken.json", 'r'))
    # print(len(broken_total))
    print(len(known_video_ids))
    # known_video_ids.extend(broken_total)
    known_video_ids = list(set(known_video_ids))
    # print(len(known_video_ids))
    with open('dMyKnown.json', 'w') as outfile:
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
    with open('dH0Poop.json', 'w') as outfile:
        json.dump(known_video_ids, outfile)


def store_differences_to_json():
    diffs = set(json.load(open('dH0Poop.json', 'r'))).difference(set(json.load(open('dMyKnown.json', 'r'))))
    diffs = diffs.difference(set(json.load(open('dBroken.json', 'r'))))
    print(len(diffs))
    with open('dDiffs.json', 'w') as outfile:
        json.dump(list(diffs), outfile)


def combine_brokens():
    union = set(json.load(open('dBroken.json', 'r'))).union(set(json.load(open('dBrokenMac.json', 'r'))))
    print(len(union))
    with open('dBroken.json', 'w') as outfile:
        json.dump(list(union), outfile)


def temp_unlisted():
    youtube = get_api_service()
    playlist_ids = ['PLXoAM842ovaAO2MHT2ZyED3Gs5Ifmdm1G']

    known_video_ids = []

    for playlist_id in playlist_ids:
        items = get_playlist_items_from_id(youtube, playlist_id)
        known_video_ids.extend(get_video_ids(items))
    known_video_ids = list(set(known_video_ids))
    print(len(known_video_ids))
    print(get_unlisteds_from_list(youtube, known_video_ids, True))
    with open('dataTempUnlisted.json', 'w') as outfile:
        json.dump(known_video_ids, outfile)


def check_existing():
    youtube = get_api_service()
    with open('dNonDelDiffs.json', 'w') as outfile:
        not_broken = filter_non_deleteds(youtube, json.load(open('dDiffs.json', 'r')))
        print(len(not_broken))
        json.dump(not_broken, outfile)


def filter_non_deleteds(youtube, ids: List[str]):
    existing = []
    i = 0
    while i < len(ids):
        j = min(i + 50, len(ids))
        for item in get_statuses_from_video_ids(youtube, ids[i:j])['items']:
            existing.append(item['id'])
        i = j
    return existing


if __name__ == "__main__":
    # my_youtube_ids_to_json()
    # other_youtube_ids_to_json()
    # store_differences_to_json()
    # temp_unlisted()
    # combine_brokens()
    check_existing()
