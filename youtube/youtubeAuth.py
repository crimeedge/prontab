# -*- coding: utf-8 -*-

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def insert_vid_into_playlist(youtube, video_id, playlist_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response


def delete_by_playlist_item_id(youtube, playlist_item_id):
    print("deleting playlistItem id %s" % playlist_item_id)
    request = youtube.playlistItems().delete(
        id=playlist_item_id
    )
    response = request.execute()
    return response


def remove_comment(youtube, comment_id):
    request = youtube.comments().delete(
        id=comment_id
    )
    response = request.execute()
    print('comment ' + comment_id + ' deleted')
    return response
