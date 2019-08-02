from makeYoutube import get_authenticated_service
import re

video_id_prog = re.compile(r'v=([^&]+)')
scope = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def get_comment_id(youtube, video_id, comment_author="Undesirable Truism"):
    request = youtube.commentThreads().list(
        part="snippet",
        searchTerms=comment_author,
        videoId=video_id
    )
    response = request.execute()
    # print (response)
    ids = []
    for item in response['items']:
        # print (item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        if item['snippet']['topLevelComment']['snippet']['authorDisplayName'] == comment_author:
            ids.append(item['id'])

    return ids


def remove_comment(youtube, id):
    request = youtube.comments().delete(
        id=id
    )
    request.execute()
    print('comment ' + id + ' deleted')


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
