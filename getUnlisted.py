import json
from typing import List

from addVideoToPlaylistSel import get_ids_from_playlist_ids
from makeYoutube import get_api_service


def get_statuses_from_video_ids(youtube, ids: List[str]):
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
        for item in get_statuses_from_video_ids(youtube, ids[i:j])['items']:
            if (item['status']['privacyStatus'] == 'unlisted')==unlist_bool:
                unlisteds.append(item['id'])
        i = j
    return unlisteds


def dump_unlisteds_from_known():
    youtube = get_api_service()
    known_file = 'dMyKnown.json'
    known_video_ids = json.load(open(known_file, 'r'))['video_ids']
    unlisteds = get_unlisteds_from_list(youtube, known_video_ids)
    print(len(unlisteds))
    with open('dMyUnlisted.json', 'w') as outfile:
        json.dump(unlisteds, outfile)


def dump_unlisteds_from_diffs():
    youtube = get_api_service()
    known_video_ids = json.load(open('dDiffs.json', 'r'))
    unlisteds = get_unlisteds_from_list(youtube, known_video_ids)
    print(len(unlisteds))
    with open('dDiffsUnlisted.json', 'w') as outfile:
        json.dump(unlisteds, outfile)


def clwi_unlisted_test():
    youtube = get_api_service()
    clwi_playlist_ids = ["PLEdfzAuIT-h7_lAhNFMgq-LTcIZvagEKY", "PLEdfzAuIT-h5_zRBPNBToV9nA2fPkHlQn",
                         "PLEdfzAuIT-h7IvAPkv65K0cy80rKqJjzs", "PLEdfzAuIT-h7LowgrtGT0g-CEJwPgpWzv",
                         "PLEdfzAuIT-h4784QAa31tEVraRpWnMCUr", "PLEdfzAuIT-h5cTZ-3tAkSYSyEnBXcQ-Zc"]
    video_ids = get_ids_from_playlist_ids(youtube, clwi_playlist_ids)
    clwi_ulist = get_unlisteds_from_list(youtube, video_ids)
    with open('clwiUnlisted.json', 'w') as outfile:
        json.dump(clwi_ulist, outfile)


if __name__ == "__main__":
    dump_unlisteds_from_known()
    # clwi_unlisted_test()
    dump_unlisteds_from_diffs()
