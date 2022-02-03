# -*- coding: utf-8 -*-
"""
@author: joeyf

\\\\\\\\\\\\\\\\\\
API CREDENTIALS 3
\\\\\\\\\\\\\\\\\\

sleep used because google API has per/sec and per/day limiters
"""
# File import
import os
import pickle
import time

from googleapiclient.discovery import build

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import googleapiclient.discovery
import googleapiclient.errors

# //////////////////////////////////////////////////////////////////////////////
# CREDENTIALS AND RELATED -- START
# //////////////////////////////////////////////////////////////////////////////

PLAYLISTID = 'PLACEHOLDER FOR PLAYLIST'
# ID is this portion :
# www.youtube.com/playlist?list= ---> PLgHkUyyNb-ckZ-8USDzSMK7o1zPqA-A_S <---

print('using cred flow 3')
credentials = None
main_api_key = 'PLACEHOLDER FOR API1'  # SWITCH CERT HERE
aux_api_key = 'PLACEHOLDER FOR API2'  # SWITCH CERT HERE

# token.pickle stores the user's credentials from previously successful logins
if os.path.exists('token3.pickle'):
    print('Loading Credentials From File...')
    with open('token3.pickle', 'rb') as token:
        credentials = pickle.load(token)

# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            'CLIENTSECRETSPLACEHOLDER.json',  # SWITCH CERT HERE TO RESPECTIVE JSON FILE NAME
            scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
        )

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token3.pickle', 'wb') as f:  # SWITCH CERT HERE
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)


# //////////////////////////////////////////////////////////////////////////////
# CREDENTIALS AND RELATED -- END
# //////////////////////////////////////////////////////////////////////////////


def delete_all_in_playlist():
    # Playlist id to track off server
    playlist_id = PLAYLISTID

    # //////////////////////////////////////////////////////////////////////////
    # SERVICE TO LIST PLAYLIST ITEMS (PUBLIC)
    # //////////////////////////////////////////////////////////////////////////

    # Create public service
    pubservice = build('youtube', 'v3', developerKey=main_api_key)
    # Requesting the contents of the linked playlist from the server
    response = pubservice.playlistItems().list(
        part='id',
        playlistId=playlist_id,
        maxResults=50
    ).execute()

    print(response)
    # Allocating the variables found
    playlistItems = response['items']

    # Looks if the server informs there is another page
    nextPageToken = response.get('nextPageToken')

    # Loops until there are no remaining pages
    while nextPageToken:
        response = pubservice.playlistItems().list(
            part='id',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        ).execute()
        print(response)
        playlistItems.extend(response['items'])
        nextPageToken = response.get('nextPageToken')

    # //////////////////////////////////////////////////////////////////////////
    # SERVICE TO DELETE PLAYLIST ITEMS (REQUIRES OAUTH 2.0)
    # //////////////////////////////////////////////////////////////////////////

    privservice = build("youtube", "v3", credentials=credentials)

    # Deletes the old contents of the playlist to ensure only new tracks are put in
    for item in playlistItems:
        time.sleep(1)
        print('Deleting {0}'.format(item['id']))
        privservice.playlistItems().delete(id=item['id']).execute()

    # Uses a try and catch because server errors arise if the playlist was already emptied
    try:
        response = pubservice.playlistItems().list(
            part='id',
            playlistId=playlist_id,
            maxResults=50
        ).execute()

        # Ensures the playlist is now empty as there were some errors in the past possibly due to network instability
        if (response.get('pageInfo')).get('totalResults') != 0:
            playlistItems = response['items']

            for item in playlistItems:
                time.sleep(1)
                print('Deleting {0}'.format(item['id']))
                privservice.playlistItems().delete(id=item['id']).execute()

    except googleapiclient.http.HttpError:
        pass
    print('Process Complete')


def add_video(video_id):
    playlist_id = PLAYLISTID

    privservice2 = build("youtube", "v3", credentials=credentials)
    r = 0
    while True and r < 10:
        try:
            request = privservice2.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "position": 0,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            response = request.execute()
            time.sleep(1)
            r += 1
        except googleapiclient.errors.HttpError:
            continue
        break

    print(response)


def search_select(Song):
    time.sleep(1)

    # Extracts the relevant information from the Song class object
    keyword = Song.title + " by " + Song.artist
    print("Searching for " + keyword)

    # //////////////////////////////////////////////////////////////////////////
    # SERVICE TO LIST PLAYLIST ITEMS (PUBLIC)
    # //////////////////////////////////////////////////////////////////////////

    # Create public service
    pubservice2 = build('youtube', 'v3', developerKey=aux_api_key)

    # Searches only one result with the given keywords
    request = pubservice2.search().list(
        part="id",
        maxResults=1,
        q=keyword
    )

    response = request.execute()
    print(response)
    song_id = ((((response.get('items'))[0]).get('id')).get('videoId'))

    return song_id
