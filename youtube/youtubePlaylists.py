from typing import List


def get_playlist_ids_list(youtube, channel_id='UCuQjQ-iqbHh-hIMrDwfYfYA'):
    request = youtube.playlists().list(
        part="id",
        maxResults=50,
        channelId=channel_id
    )
    ids = []
    while request:
        response = request.execute()
        ids.extend([item['id'] for item in response['items']])
        request = youtube.playlistItems().list_next(request, response)

    return ids


def get_playlist_ids_title_dict(youtube, channel_id='UCuQjQ-iqbHh-hIMrDwfYfYA'):
    request = youtube.playlists().list(
        part="id,snippet",
        maxResults=50,
        channelId=channel_id
    )
    ids = dict()
    while request:
        response = request.execute()
        for item in response['items']:
            ids[item["id"]] = item["snippet"]["title"]
        request = youtube.playlistItems().list_next(request, response)

    return ids


def get_playlist_ids_count_dict(youtube, channel_id='UCuQjQ-iqbHh-hIMrDwfYfYA'):
    request = youtube.playlists().list(
        part="id,contentDetails",
        maxResults=50,
        channelId=channel_id
    )
    ids_counts = dict()
    while request:
        response = request.execute()
        for item in response['items']:
            ids_counts[item['id']] = item['contentDetails']['itemCount']
        request = youtube.playlistItems().list_next(request, response)

    return ids_counts


def get_playlist_ids_count_dict_from_list(youtube, ids: List[str]):
    ids_str = ','.join(ids)
    request = youtube.playlists().list(
        part="id,contentDetails",
        maxResults=50,
        id=ids_str
    )
    ids_counts = dict()
    while request:
        response = request.execute()
        for item in response['items']:
            ids_counts[item['id']] = item['contentDetails']['itemCount']
        request = youtube.playlistItems().list_next(request, response)

    return ids_counts
