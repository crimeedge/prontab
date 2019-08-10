from typing import List


def _get_statuses_from_video_ids(youtube, ids: List[str]):
    ids_str = ','.join(ids)
    request = youtube.videos().list(
        part="status",
        id=ids_str
    )
    response = request.execute()

    return response


def get_unlisteds_from_list(youtube, ids: List[str],unlist_bool=True):
    unlisteds = []
    i = 0
    while i < len(ids):
        j = min(i + 50, len(ids))
        for item in _get_statuses_from_video_ids(youtube, ids[i:j])['items']:
            if (item['status']['privacyStatus'] == 'unlisted') == unlist_bool:
                unlisteds.append(item['id'])
        i = j
    return unlisteds


def _get_id_from_video_ids(youtube, ids: List[str]):
    ids_str = ','.join(ids)
    request = youtube.videos().list(
        part="id",
        id=ids_str
    )
    response = request.execute()

    return response


def filter_privates_from_vid_list_old(youtube, ids: List[str]):
    print(len(ids))
    filtereds = []
    i = 0
    while i < len(ids):
        j = min(i + 50, len(ids))
        for item in _get_id_from_video_ids(youtube, ids[i:j])['items']:
            filtereds.append(item['id'])
        i = j
    print(len(filtereds))
    return filtereds


def _get_content_details_from_video_ids(youtube, ids: List[str]):
    ids_str = ','.join(ids)
    request = youtube.videos().list(
        part="id,contentDetails",
        id=ids_str
    )
    response = request.execute()

    return response


def filter_restricteds_from_vid_list(youtube, ids: List[str]):
    print(len(ids))
    filtereds = []
    i = 0
    while i < len(ids):
        j = min(i + 50, len(ids))
        for item in _get_content_details_from_video_ids(youtube, ids[i:j])['items']:
            if "regionRestriction" not in item['contentDetails']:
                filtereds.append(item['id'])
            elif "blocked" in item['contentDetails']['regionRestriction']:
                if "US" not in item['contentDetails']['regionRestriction']["blocked"]:
                    print(item['contentDetails']['regionRestriction'])
                    filtereds.append(item['id'])
            elif "US" in item['contentDetails']['regionRestriction']["allowed"]:
                print(item['contentDetails']['regionRestriction'])
                filtereds.append(item['id'])
        i = j
    print(len(filtereds))
    return filtereds
