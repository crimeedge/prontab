from youtube.youtubeComments import get_comment_id
from youtube.youtubeMake import get_authenticated_service

from youtube.youtubeAuth import remove_comment
from progs import video_id_prog

scope = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    youtube = get_authenticated_service(scope)
    while True:
        url = input("url to kill all comments:")
        if video_id_prog.search(url):
            # print (video_id_prog.search(url).group(1))
            ids = get_comment_id(youtube, video_id_prog.search(url).group(1))
            # print(ids)
            for id in ids:
                remove_comment(youtube, id)


if __name__ == '__main__':
    main()
