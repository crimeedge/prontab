# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import sys
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    # client_secrets_file = sys.argv[1]

    # # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()

    key=open('.creds').readlines()[0].strip()

    # youtube = googleapiclient.discovery.build(
        # api_service_name, api_version, credentials=credentials,developerKey=key)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id="UCuQjQ-iqbHh-hIMrDwfYfYA"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()