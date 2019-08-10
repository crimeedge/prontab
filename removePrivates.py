# -*- coding: utf-8 -*-

from googleapiclient.errors import HttpError

from youtube.youtubeMake import get_authenticated_service, default_scope
from youtube.youtubeAuth import delete_by_playlist_item_id
from youtube.youtubePlaylistItems import get_playlist_items_from_id
from youtube.youtubePlaylists import get_playlist_ids_list


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


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

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


if __name__ == "__main__":
    main()
    # youtube = get_api_service()
    # listy = get_playlist_ids_count_dict(youtube, 'UCzjiyMpyPuHnQyVFp9Nimbg')
    # print(listy)
    # print(len(listy))
