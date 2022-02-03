"""
Created on Thu Jan 27 00:17:25 2022

@author: joeyf

This is to pull tracks from a spotify "Share this playlist" URL using spotipy

It converts the long and complex song objects pulled from the API to simple "Song object" consisting of the unique
Spotify song ID, the song title, and the song artists

It then stores the listed songs in a file called depot.txt (I used this because the purpose of this project was to
download Spotify playlists) and before storing the songs into the output array, it will verify that it isn't in the
depot.txt file.

Any credentials pertaining to the Spotify API have been removed since the program is still in use

"""
import spotipy
import os
import time
from spotipy.oauth2 import SpotifyClientCredentials

# This is the credentials of the API access I am using
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="CLIENT ID PLACEHOLDER",
                                                           client_secret="CLIENT SECRET PLACEHOLDER"))


# This standardizes the tracks to only the relevant information using the Song constructor class
def Track_Organization(track_id):
    # This extracts the track object from the spotify server
    track = sp.track("spotify:track:" + track_id)

    # This pulls the song name from the track object
    song_name = track.get('name')

    # This pulls the artist list object from the track object

    artists = track.get('artists')
    # Instantiations for the loop
    all_artists = ""
    i = 0

    # This loop adds all the artist names together by pulling from the dictionary objects in the list object indexes
    for i in range(len(artists)):
        if i == 0:
            all_artists = ((artists[i]).get('name', 'N/A'))
        else:
            all_artists += (", " + (artists[i]).get('name', 'N/A'))
    return Song(track_id, song_name, all_artists)


# This is the way track objects will be formatted
class Song:
    def __init__(self, ID, title, artist):
        self.ID = ID
        self.title = title
        self.artist = artist

    # This takes the shareable link and extracts the ID to the object type


def extract_playlist_id_from_hyperlink(playlist_hyperlink):
    # The ID is consistently between this index
    ID = playlist_hyperlink[34:56]
    return ID


# This uses a file called Depot.txt to verify if a song is in the repository already and adds it if it's missing
def Song_Addition(playlist_hyperlink):
    # Uses the function to specifically assign the ID to the variable
    ID = extract_playlist_id_from_hyperlink(playlist_hyperlink)

    # The api recognizes IDs in this format
    pl_id = f'spotify:playlist:{ID}'

    # This queries the spotify server for the playlist contents
    offset = 0
    response = sp.playlist_items(pl_id, offset=offset, fields='items.track.id,total', additional_types=['track'])

    # Pulls only the info we care about
    playlist = response.get('items', 'error')

    # This shows if query result and spotify server known data matchup
    if len(playlist) == response['total']:
        pass

    else:
        # This limits the while loop to 10 attempts because the Spotify API has a query/per sec limit
        attempt = 0

        while (len(playlist) != response['total']) and attempt < 10:

            # The sleep was also implemented to avoid server shut out errors
            time.sleep(1)
            print("Attempting to retrieve remaining songs...")

            # Spotify API has a limit of 100 per page, this ensures that up to 1000 tracks can be stored
            offset += 100

            # The new requests are associated to response2 and added to the playlist list
            response2 = sp.playlist_items(pl_id, offset=offset, fields='items.track.id,total',
                                          additional_types=['track'])
            playlist2 = response2.get('items', 'error')
            playlist.extend(playlist2)

    # This is the final check for the content in the playlist list
    if len(playlist) == response['total']:
        print("Worked with no issues")
    else:
        print("certain issues identified, proceeding with " + len(playlist) + " songs out of " + response['total'])

    # Checking if file exists, creating it if not
    file = open("Depot.txt", "a+")
    file.close()

    # The list attributed to the songs that need to be downloaded
    queue = []

    # Goes through each individual track object in the playlist and attributes it to new or ignore group
    try:
        i = 0
        for i in range(len(playlist)):

            # Fills the queue array with the Song objects for every new song added to depot.txt (new playlist
            # items since last use)
            if len(((playlist[i]).get('track')).get('id')) > 10:
                string = ((playlist[i]).get('track')).get('id')
                with open("Depot.txt", "r+") as f:
                    line_found = any(string in line for line in f)
                    if not line_found:
                        f.seek(0, os.SEEK_END)
                        f.write(string + "\n")
                        queue.append(Track_Organization(string))
                        print(f'Adding {(Track_Organization(string)).title}')

    # Filters out TypeError because an empty object or error can cause a stop
    except TypeError:
        pass

    finally:
        f.close()

    return queue


# This function is to remove specific song IDs from depot in the event the last song batch wasn't complete
def Song_Removal(Song):
    # Import the missed songs array of Song objects
    song_id_array = []
    file = open("newDepot.txt", "a+")
    file.close()
    i = 0

    # Fill the song_id.. list with the same content as the Song list
    for i in range(len(Song)):
        song_id_array.append(Song[i].ID)
        print(Song[i].ID)
        print(f'Removing {Song[i].title}')
    print(song_id_array)
    print(len(song_id_array))

    # Opens a new file, and transfers the lines in the old depot.txt file to the new file if the individual lines don't
    # contain the IDs found in the missed songs, that way only completed objects are transferred
    try:
        with open('Depot.txt') as oldfile, open('newDepot.txt', 'w+') as newfile:
            for line in oldfile:
                if not any(missed_songs in line for missed_songs in song_id_array):
                    newfile.write(line)

    except TypeError:
        pass

    # Closes the new file and renames it to depot so future iterations of the main code refer to this instead
    finally:
        newfile.close()
        try:
            print("Deleting Depot.txt......")
            os.remove("Depot.txt")
        except FileNotFoundError:
            print("File not found")
            pass
        os.rename('newDepot.txt', 'Depot.txt')
        print('file renamed...')
