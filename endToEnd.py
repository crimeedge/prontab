from addVideoToPlaylistSel import make_tuple_diffs, add_diffs
from driverMethods import create_driver
from hvidsYoutubeIds import get_hvids_by_sel
from storeAllVideoIds import my_youtube_ids_to_json, other_youtube_ids_to_json
from youtube.youtubeMake import get_api_service


def main():
    while True:
        my_youtube_ids_to_json()
        y = get_api_service()
        # poop
        other_youtube_ids_to_json(y, ['LLzjiyMpyPuHnQyVFp9Nimbg'], ['UCzjiyMpyPuHnQyVFp9Nimbg'], [],
                                  'dPoop.json')
        # H0
        other_youtube_ids_to_json(y, ['LLhNOMudRAcLnj6hlCLjLk9A'], ["UChNOMudRAcLnj6hlCLjLk9A"], [], 'dH0.json')
        # vsh
        other_youtube_ids_to_json(y, [], [], ['FLt5AE3F1yzn2IsASa55-c3Q', 'PL4X95Lb2XkAG3zaVxwgu2A-3s46n8hsIG'],
                                  "dVsh.json")
        driver = create_driver()
        get_hvids_by_sel(driver, "https://www.hvids.net/viewforum.php?f=21&start=", "dHvidsMakeover.json")
        get_hvids_by_sel(driver, 'https://www.hvids.net/viewforum.php?f=19&start=', "dHvidsBuzzcut.json")
        get_hvids_by_sel(driver, "https://www.hvids.net/viewforum.php?f=39&start=", "dHvidsCharity.json")
        driver.quit()

        if make_tuple_diffs() <= 0:
            break
        add_diffs('dDiffs.json')


if __name__ == "__main__":
    main()
