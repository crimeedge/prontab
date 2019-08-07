from collections import defaultdict
from typing import List

from datetime import datetime
import dateutil.parser

from getUnlisted import get_unlisteds_from_list, get_statuses_from_video_ids
from removePrivates import get_playlist_ids_list, get_playlist_items_from_id, get_video_ids, \
    filter_private_playlist_items, get_playlist_ids_count_dict
from makeYoutube import get_authenticated_service, get_api_service

import json

from pprint import PrettyPrinter


def my_youtube_ids_to_json():
    youtube = get_api_service()

    playlist_ids_dict = get_playlist_ids_count_dict(youtube,channel_id='UCuQjQ-iqbHh-hIMrDwfYfYA')

    # cached_dict = defaultdict(lambda:-1,dict())
    # known_video_ids=[]
    cached_dict = defaultdict(lambda:-1, json.load(open('dMyKnown.json', 'r')) )
    known_video_ids = cached_dict['video_ids']

    for playlist_id in playlist_ids_dict:
        if playlist_ids_dict[playlist_id]>cached_dict[playlist_id]:
            print(playlist_id)
            items = get_playlist_items_from_id(youtube, playlist_id)
            known_video_ids.extend(get_video_ids(items))

    known_video_ids = list(set(known_video_ids))
    print(len(known_video_ids))
    playlist_ids_dict['video_ids'] = known_video_ids
    with open('dMyKnown.json', 'w') as outfile:
        json.dump(playlist_ids_dict, outfile)


def other_youtube_ids_to_json():
    youtube = get_api_service()

    # cached_dict = defaultdict(lambda:-1,dict())
    # cached_dict['LLhNOMudRAcLnj6hlCLjLk9A']="2019-08-01"
    # cached_dict['LLzjiyMpyPuHnQyVFp9Nimbg'] = "2019-08-01"
    # known_video_ids = json.load(open('dH0Poop.json', 'r'))
    cached_dict = defaultdict(lambda: -1, json.load(open('dH0Poop.json', 'r')))
    known_video_ids = cached_dict['video_ids']
    # h0 liked, poop liked
    liked_playlist_ids = ['LLhNOMudRAcLnj6hlCLjLk9A', 'LLzjiyMpyPuHnQyVFp9Nimbg']
    liked_playlist_ids_dict = dict()

    for liked_id in liked_playlist_ids:

        liked_playlist_ids_dict[liked_id] = str(datetime.today())
        items = filter_private_playlist_items(get_playlist_items_from_liked_id(youtube, liked_id,cached_dict[liked_id]), False)
        print(len(items))
        known_video_ids.extend(get_video_ids(items))

    playlist_ids_dict=dict()
    # h0 channel
    playlist_ids_dict.update(get_playlist_ids_count_dict(youtube, "UChNOMudRAcLnj6hlCLjLk9A"))
    # poop channel
    playlist_ids_dict.update(get_playlist_ids_count_dict(youtube, 'UCzjiyMpyPuHnQyVFp9Nimbg'))

    for playlist_id in playlist_ids_dict:
        if playlist_ids_dict[playlist_id]>cached_dict[playlist_id]:
            print(playlist_id)
            items = filter_private_playlist_items(get_playlist_items_from_id(youtube, playlist_id),False)
            known_video_ids.extend(get_video_ids(items))

    known_video_ids = list(set(known_video_ids))
    print(len(known_video_ids))
    playlist_ids_dict['video_ids'] = known_video_ids
    playlist_ids_dict.update(liked_playlist_ids_dict)

    # PrettyPrinter().pprint(playlist_ids_dict)
    with open('dH0Poop.json', 'w') as outfile:
        json.dump(playlist_ids_dict, outfile)


def _parse_date(string):
    dt = dateutil.parser.parse(string)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=dateutil.tz.UTC)
    return dt


def get_playlist_items_from_liked_id(youtube, playlist_id="LLzjiyMpyPuHnQyVFp9Nimbg",after_date="2019-05-01"):
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlist_id
    )
    items = []
    while request:
        response = request.execute()
        items += response["items"]
        if _parse_date( response["items"][-1]["snippet"]["publishedAt"]) < _parse_date(after_date):
            request = None
        else:
            request = youtube.playlistItems().list_next(request, response)

    return items


def store_differences_to_json():
    diffs = set(json.load(open('dH0Poop.json', 'r'))['video_ids']).difference(set(json.load(open('dMyKnown.json', 'r'))['video_ids']))
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
    store_differences_to_json()
    # temp_unlisted()
    # combine_brokens()
    # check_existing()
    # print(len(get_playlist_items_from_liked_id(get_api_service())))
