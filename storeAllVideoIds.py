from collections import defaultdict

from datetime import datetime

from removePrivates import get_video_ids, \
    filter_private_playlist_items
from youtube.youtubePlaylistItems import get_playlist_items_from_id, get_playlist_items_from_liked_id
from youtube.youtubePlaylists import get_playlist_ids_count_dict, \
    get_playlist_ids_count_dict_from_list
from youtube.youtubeMake import get_api_service

import json


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


def other_youtube_ids_to_json(youtube=get_api_service(),liked_playlist_ids=[],channel_ids=[],free_playlist_ids=[],filename='dH0PoopVsh.json'):

    # cached_dict = defaultdict(lambda:-1,dict())
    # cached_dict['LLhNOMudRAcLnj6hlCLjLk9A']="2019-08-01"
    # cached_dict['LLzjiyMpyPuHnQyVFp9Nimbg'] = "2019-08-01"
    # known_video_ids = json.load(open('dH0PoopVsh.json', 'r'))
    cached_dict = defaultdict(lambda: -1, json.load(open(filename, 'r')))
    known_video_ids = cached_dict['video_ids']

    # h0 liked, poop liked
    # liked_playlist_ids = ['LLhNOMudRAcLnj6hlCLjLk9A', 'LLzjiyMpyPuHnQyVFp9Nimbg']
    liked_playlist_ids_dict = dict()

    for liked_id in liked_playlist_ids:

        liked_playlist_ids_dict[liked_id] = str(datetime.today())
        items = filter_private_playlist_items(
            get_playlist_items_from_liked_id(youtube, liked_id, cached_dict[liked_id]), False)
        print(len(items))
        known_video_ids.extend(get_video_ids(items))

    playlist_ids_dict=dict()
    # h0 channel,poop channel
    # channel_ids=["UChNOMudRAcLnj6hlCLjLk9A",'UCzjiyMpyPuHnQyVFp9Nimbg']
    for channel_id in channel_ids:
        playlist_ids_dict.update(get_playlist_ids_count_dict(youtube, channel_id))

    # vsh
    # free_playlist_ids = ['FLt5AE3F1yzn2IsASa55-c3Q', 'PL4X95Lb2XkAG3zaVxwgu2A-3s46n8hsIG']
    playlist_ids_dict.update(get_playlist_ids_count_dict_from_list(youtube,free_playlist_ids))

    for playlist_id in playlist_ids_dict:
        if playlist_ids_dict[playlist_id]>cached_dict[playlist_id]:
            print(playlist_id)
            items = filter_private_playlist_items(get_playlist_items_from_id(youtube, playlist_id),False)
            print(len(items))
            known_video_ids.extend(get_video_ids(items))

    known_video_ids = list(set(known_video_ids))
    print(len(known_video_ids))
    playlist_ids_dict['video_ids'] = known_video_ids
    playlist_ids_dict.update(liked_playlist_ids_dict)

    # PrettyPrinter().pprint(playlist_ids_dict)
    with open(filename, 'w') as outfile:
        json.dump(playlist_ids_dict, outfile)


def combine_brokens():
    union = set(json.load(open('dBroken.json', 'r'))).union(set(json.load(open('dBrokenMac.json', 'r'))))
    print(len(union))
    with open('dBroken.json', 'w') as outfile:
        json.dump(list(union), outfile)


if __name__ == "__main__":
    # combine_brokens()
    my_youtube_ids_to_json()
    y=get_api_service()
    # poop
    other_youtube_ids_to_json(y, ['LLzjiyMpyPuHnQyVFp9Nimbg'], ['UCzjiyMpyPuHnQyVFp9Nimbg'], [],
                              'dPoop.json')
    # H0
    other_youtube_ids_to_json(y,['LLhNOMudRAcLnj6hlCLjLk9A'],["UChNOMudRAcLnj6hlCLjLk9A"],[],'dH0.json')
    # vsh
    other_youtube_ids_to_json(y,[],[],['FLt5AE3F1yzn2IsASa55-c3Q', 'PL4X95Lb2XkAG3zaVxwgu2A-3s46n8hsIG'],"dVsh.json")
