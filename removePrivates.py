# -*- coding: utf-8 -*-
import json

from googleapiclient.errors import HttpError
from youtube.youtubeMake import get_authenticated_service, default_scope, get_api_service
from youtube.youtubeAuth import delete_by_playlist_item_id
from youtube.youtubePlaylistItems import get_playlist_items_from_id
from youtube.youtubePlaylists import get_playlist_ids_list, get_playlist_ids_title_dict
from youtube.youtubeVideos import update_vid_playlist_insertion_dict


def filter_private_playlist_items(items, get_privates=True):
    filtered_items = []
    for item in items:
        # print(item['snippet']['title'])
        if (item['snippet']['title'] == 'Private video') == get_privates:
            filtered_items.append(item)
    return filtered_items


def filter_private_playlist_item_ids(items, get_privates=True):
    return get_id_from_items(filter_private_playlist_items(items, get_privates))


def get_id_from_items(items):
    return [item['id'] for item in items]


def get_video_ids(items):
    video_ids = []
    for item in items:
        # print(item['snippet']['title'])
        video_ids.append(item['snippet']['resourceId']['videoId'])
    return video_ids


def remove_privates_by_api():
    youtube = get_authenticated_service(default_scope)
    playlist_ids = get_playlist_ids_list(youtube)
    count = 0
    for playlist_id in playlist_ids:
        items = get_playlist_items_from_id(youtube, playlist_id)
        privates = filter_private_playlist_item_ids(items)
        for playlist_item_id in privates:
            try:
                print(playlist_item_id)
                delete_by_playlist_item_id(youtube, playlist_item_id)
                count += 1
            except HttpError as err:
                print(err)
    print('number of videos del33ted: %s', count)


def move_into_blacklist(playlist_ids=get_playlist_ids_title_dict(get_api_service())):
    youtube = get_api_service()
    # dBlacklistedVids.json, APIUnlisted
    already_blacklist = ['PLXoAM842ovaBTZajyyFHcIYqtrCP7SBcI', 'PLXoAM842ovaAO2MHT2ZyED3Gs5Ifmdm1G']
    bad_names = ["dBlacklistedVids.json","dLQ.json0","dLQ.json1","dLQ.json2"]

    set_adds = set()
    for playlist_id in playlist_ids:
        if playlist_id not in already_blacklist:
            items = get_playlist_items_from_id(youtube, playlist_id)
            vid_dict = {item['snippet']['resourceId']['videoId']: "None" for item in items}
            vid_dict = update_vid_playlist_insertion_dict(youtube, vid_dict)
            for item in items:
                if vid_dict[item['snippet']['resourceId']['videoId']] in bad_names  :
                    set_adds.add(
                        (item['snippet']['resourceId']['videoId'], vid_dict[item['snippet']['resourceId']['videoId']]))
                    # TODO: figure out how to get original playlist's name
                    set_adds.add((item['snippet']['resourceId']['videoId'], playlist_ids[playlist_id]))
                    # print('set_adds:'+str(len(set_adds)))
            print(playlist_ids[playlist_id])
        # if len(set_adds)>2:
        #     print(set_adds)
        #     break
    # next, call add_diffs
    json.dump(list(set_adds), open('dBlacklistedVids.json', 'w'))


# def move_into_lq():
#     youtube = get_api_service()
#     playlist_ids = {'PLXoAM842ovaBhnS-JAtoRfLWdUIJRFhWR':'APIH0Poop-7'}
#     set_adds = set()
#     for playlist_id in playlist_ids:
#         items = get_playlist_items_from_id(youtube, playlist_id)
#         # fix this shit and write more generalizable methonds GDI
#         vid_dict = {item['snippet']['resourceId']['videoId']: "None" for item in items}
#         vid_dict = update_vid_playlist_insertion_dict(youtube, vid_dict)
#         for item in items:
#             if vid_dict[item['snippet']['resourceId']['videoId']] == "dBlacklistedVids.json":
#                 set_adds.add((item['snippet']['resourceId']['videoId'], "dBlacklistedVids.json"))
#                 set_adds.add((item['snippet']['resourceId']['videoId'], playlist_ids[playlist_id]))
#         print(playlist_ids[playlist_id])
#         # if len(set_adds)>2:
#         #     print(set_adds)
#         #     break
#     # next, call add_diffs
#     json.dump(list(set_adds), open('dLQ.json', 'w'))


if __name__ == "__main__":
    # remove_privates_by_api()
    move_into_blacklist(playlist_ids={'PLXoAM842ovaBhnS-JAtoRfLWdUIJRFhWR': 'APIH0Poop-7',
                                      'PLXoAM842ovaDcAvScYKXgaThVIghj-7Jh': 'APIH0Poop-6',
                                      'PLXoAM842ovaD0BtaoEQis7acO0LPGP8_e': 'dH0.json',
                                      'PLXoAM842ovaDV60ezZW9ZuxeNks66umS6':'dPoop.json',
                                      'PLXoAM842ovaDOp0guagmY96SCZeg2kB2A':'dHvidsBuzzcut.json'})
    # addVideoToPlaylistSel.add_diffs('dBlacklistedVids.json')
    # youtube = get_api_service()
    # listy = get_playlist_ids_count_dict(youtube, 'UCzjiyMpyPuHnQyVFp9Nimbg')
    # print(listy)
    # print(len(listy))
