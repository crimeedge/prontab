import json

from driverMethods import create_driver
from youtube.youtubeMake import get_api_service
from progs import video_id_prog, youtube_prog, be_prog
from youtube.youtubeVideos import filter_privates_from_vid_list


def get_ids_from_hvids_filename(filename):
    lines = [line.rstrip('\n') for line in open(filename, 'r')]
    return parse_ids_from_list(lines)


def parse_ids_from_list(sublist):
    ids = []
    for line in sublist:
        if youtube_prog.search(line):
            if video_id_prog.search(line):
                search_id = video_id_prog.search(line).group(1)
                if not len(search_id) == 11:
                    print(search_id)
                    search_id=search_id[:11]
                ids.append(search_id)
        elif be_prog.search(line):
            search_id = be_prog.search(line).group(1)
            if not len(search_id) == 11:
                print(search_id)
                search_id = search_id[:11]
            ids.append(search_id)
    ids = list(set(ids))
    print(len(ids))
    return ids


def get_hvids_by_sel(driver, hvids_url="https://www.hvids.net/viewforum.php?f=21&start=",
                     filename="dHvidsMakeover.json"):
    try:
        known_video_ids = json.load(open(filename, 'r'))['video_ids']
    except FileNotFoundError:
        print("filename not found kvi is empty")
        known_video_ids = []

    new_video_ids = []
    i = 0
    while i < 1550:
        driver.get(hvids_url + str(i))
        hvids_list = driver.execute_script(open('getUnreadPPB.js').read())
        new_video_ids.extend(parse_ids_from_list(hvids_list))
        print(hvids_list)
        i+=50
        if len(hvids_list) == 0:
            break

    new_video_ids = list(set(new_video_ids).difference(set(known_video_ids)))
    youtube = get_api_service()
    known_video_ids.extend(filter_privates_from_vid_list(youtube, new_video_ids))

    vdict = dict()
    vdict['video_ids'] = known_video_ids
    json.dump(vdict,open(filename, 'w'))


if __name__ == '__main__':
    driver = create_driver()
    get_hvids_by_sel(driver,"https://www.hvids.net/viewforum.php?f=21&start=","dHvidsMakeover.json")
    get_hvids_by_sel(driver,'https://www.hvids.net/viewforum.php?f=19&start=',"dHvidsBuzzcut.json")
    get_hvids_by_sel(driver,"https://www.hvids.net/viewforum.php?f=39&start=","dHvidsCharity.json")
    driver.quit()
