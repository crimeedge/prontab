import json

from addVideoToPlaylistSel import get_ids_from_playlist_ids
from removePrivates import get_video_ids
from youtube.youtubeMake import get_api_service
from youtube.youtubePlaylistItems import get_playlist_items_from_id
from youtube.youtubeVideos import get_unlisteds_from_list


def clwi_unlisted_test():
    youtube = get_api_service()
    clwi_playlist_ids = ["PLEdfzAuIT-h7_lAhNFMgq-LTcIZvagEKY", "PLEdfzAuIT-h5_zRBPNBToV9nA2fPkHlQn",
                         "PLEdfzAuIT-h7IvAPkv65K0cy80rKqJjzs", "PLEdfzAuIT-h7LowgrtGT0g-CEJwPgpWzv",
                         "PLEdfzAuIT-h4784QAa31tEVraRpWnMCUr", "PLEdfzAuIT-h5cTZ-3tAkSYSyEnBXcQ-Zc"]
    video_ids = get_ids_from_playlist_ids(youtube, clwi_playlist_ids)
    clwi_ulist = get_unlisteds_from_list(youtube, video_ids)
    with open('clwiUnlisted.json', 'w') as outfile:
        json.dump(clwi_ulist, outfile)


def temp_api_unlisted():
    youtube = get_api_service()
    playlist_ids = ['PLXoAM842ovaAO2MHT2ZyED3Gs5Ifmdm1G']

    known_video_ids = []

    for playlist_id in playlist_ids:
        items = get_playlist_items_from_id(youtube, playlist_id)
        known_video_ids.extend(get_video_ids(items))
    known_video_ids = list(set(known_video_ids))
    print(len(known_video_ids))
    # print(get_unlisteds_from_list(youtube, known_video_ids, False))
    with open('dAPIUnlisted.json', 'w') as outfile:
        json.dump(known_video_ids, outfile)


def dump_unlisteds_from_known():
    youtube = get_api_service()
    known_video_ids = json.load(open('dMyKnown.json', 'r'))['video_ids']
    unlisteds = get_unlisteds_from_list(youtube, known_video_ids)
    print(len(unlisteds))
    with open('dMyAllUnlisted.json', 'w') as outfile:
        json.dump(unlisteds, outfile)


def dump_unlisteds_from_diffs():
    youtube = get_api_service()
    known_video_ids = [tupl[0] for tupl in json.load(open('dDiffs.json', 'r'))]
    unlisteds = get_unlisteds_from_list(youtube, known_video_ids)
    print(len(unlisteds))
    with open('dDiffsUnlisted.json', 'w') as outfile:
        json.dump(unlisteds, outfile)


def print_differences_of_unlisted():
    diffs_unlisted=set(json.load(open('dDiffsUnlisted.json', 'r')))
    my_all_unlisted=set(json.load(open('dMyAllUnlisted.json', 'r')))
    combined_unlisted=diffs_unlisted.union(my_all_unlisted)
    not_in_api_unlisted = combined_unlisted.difference(set(json.load(open('dAPIUnlisted.json', 'r'))))
    u_diffs = [(niau,'APIUnlisted') for niau in not_in_api_unlisted]
    print(len(u_diffs))
    print(u_diffs)
    with open('dUDiffs.json', 'w') as outfile:
        json.dump(u_diffs, outfile)


if __name__ == "__main__":
    # temp_api_unlisted()
    # dump_unlisteds_from_known()
    # dump_unlisteds_from_diffs()
    print_differences_of_unlisted()
