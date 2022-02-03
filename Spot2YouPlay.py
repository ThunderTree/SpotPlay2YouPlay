# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 22:09:16 2022

@author: joeyf

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
THIS IS THE MAIN PAGE
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

Requests the playlist hyperlink and send it over to the spotifyAPI page that organizes the information and returns a
list of the Song Constructor class defined in the SpotifyAPI. This song list is queried in YouTube search and the first
result is added to a designated YouTube User playlist, defined in the YoutubeAPI pages. There are multiple API pages
with a somewhat recursive main function because when a quota is maxed, it will switch to different credentials

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
IMPORTANT YOUTUBE API INFORMATION
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

Follow the directions of this video to set up the YouTube APIs the same way:
https://www.youtube.com/watch?v=vQQEaSnQ_bs&t=529s
Specifically the web app and the specified 8080 port.

ONLY REQUEST THIS SCOPE: https://www.googleapis.com/auth/youtube.force-ssl
"""
import SpotifyAPI
import YoutubeAPI3
import YoutubeAPI2
import YoutubeAPI
import os
import googleapiclient.errors
import datetime


def main():
    complete = 0
    HYPERLINK = input("Paste the entire playlist hyperlink: ")
    new_songs = SpotifyAPI.Song_Addition(HYPERLINK)
    remaining_songs = new_songs

    if complete == 0:
        try:
            YoutubeAPI.delete_all_in_playlist()  # HERE WAS CHANGED FROM '' TO '2' OR '2' TO '3'
            complete = 1

        except googleapiclient.http.HttpError:
            complete = 0

    scope = len(new_songs)
    i = 0
    try:
        for i in range(scope):
            YoutubeAPI.add_video(
                (YoutubeAPI.search_select(new_songs[i])))  # HERE WAS CHANGED FROM '' TO '2' OR '2' TO '3'
            remaining_songs = new_songs[i:-1]

    except googleapiclient.http.HttpError:
        print("The quota for today has been maxed .... printing the missed songs")
        print(remaining_songs)

        file = open('Depot.txt', 'r')
        original_depot_length = 0
        for line in file:
            if line != "\n":
                original_depot_length += 1
        file.close()

        print(f"Original items in file before removal: {original_depot_length}")

        SpotifyAPI.Song_Removal(remaining_songs)

        print('The number of remaining songs is ' + str(
            len(remaining_songs)) + ', the total amount of new songs is ' + str(
            len(new_songs)) + ', therefore there should be ' + str(
            original_depot_length - (len(new_songs) - len(remaining_songs))) + 'items remaining')

        file = open('Depot.txt', 'r')
        new_depot_length = 0
        for line in file:
            if line != "\n":
                new_depot_length += 1
        file.close()

        print(f'There are {new_depot_length} items remaining')
        print('Switching to second API')
        main2(HYPERLINK, complete)


def main2(Hyperlink, complete):
    HYPERLINK = Hyperlink
    new_songs = SpotifyAPI.Song_Addition(HYPERLINK)
    remaining_songs = new_songs

    if complete == 0:
        try:
            YoutubeAPI2.delete_all_in_playlist()  # HERE WAS CHANGED FROM '' TO '2' OR '2' TO '3'
            complete = 1

        except googleapiclient.http.HttpError:
            complete = 0

    scope = len(new_songs)
    i = 0
    try:
        for i in range(scope):
            YoutubeAPI2.add_video(
                (YoutubeAPI2.search_select(new_songs[i])))  # HERE WAS CHANGED FROM '' TO '2' OR '2' TO '3'
            remaining_songs = new_songs[i:-1]

    except googleapiclient.http.HttpError:
        print("The quota for today has been maxed .... printing the missed songs")
        print(remaining_songs)

        file = open('Depot.txt', 'r')
        original_depot_length = 0
        for line in file:
            if line != "\n":
                original_depot_length += 1
        file.close()

        print(f"Original items in file before removal: {original_depot_length}")

        SpotifyAPI.Song_Removal(remaining_songs)

        print('The number of remaining songs is ' + str(
            len(remaining_songs)) + ', the total amount of new songs is ' + str(
            len(new_songs)) + ', therefore there should be ' + str(
            original_depot_length - (len(new_songs) - len(remaining_songs))) + 'items remaining')

        file = open('Depot.txt', 'r')
        new_depot_length = 0
        for line in file:
            if line != "\n":
                new_depot_length += 1
        file.close()

        print(f'There are {new_depot_length} items remaining')
        print('Switching to third API')
        main3(HYPERLINK, complete)


def main3(Hyperlink, complete):
    HYPERLINK = Hyperlink
    new_songs = SpotifyAPI.Song_Addition(HYPERLINK)
    remaining_songs = new_songs

    if complete == 0:
        try:
            YoutubeAPI3.delete_all_in_playlist()  # HERE WAS CHANGED FROM '' TO '2' OR '2' TO '3'
            complete = 1

        except googleapiclient.http.HttpError:
            complete = 0

    scope = len(new_songs)
    i = 0
    try:
        for i in range(scope):
            YoutubeAPI3.add_video(
                (YoutubeAPI3.search_select(new_songs[i])))  # HERE WAS CHANGED FROM '' TO '2' OR '2' TO '3'
            remaining_songs = new_songs[i:-1]

    except googleapiclient.http.HttpError:
        print("The quota for today has been maxed .... printing the missed songs")
        print(remaining_songs)

        file = open('Depot.txt', 'r')
        original_depot_length = 0
        for line in file:
            if line != "\n":
                original_depot_length += 1
        file.close()

        print(f"Original items in file before removal: {original_depot_length}")

        SpotifyAPI.Song_Removal(remaining_songs)

        print('The number of remaining songs is ' + str(
            len(remaining_songs)) + ', the total amount of new songs is ' + str(
            len(new_songs)) + ', therefore there should be ' + str(
            original_depot_length - (len(new_songs) - len(remaining_songs))) + 'items remaining')

        file = open('Depot.txt', 'r')
        new_depot_length = 0
        for line in file:
            if line != "\n":
                new_depot_length += 1
        file.close()

        next_day = str(datetime.date.today() + datetime.timedelta(days=1))

        print(f'There are {new_depot_length} items remaining')
        print('Re-enter the same playlist after 3am on ' + next_day)

# By deleting the Depot, this function makes it so that previously downloaded songs can get downloaded again
def refresh():
    try:
        print("Deleting Depot.txt......")
        os.remove("Depot.txt")
    except FileNotFoundError:
        print("File not found")
        pass


# refresh()

# main()


"""

Need to add an incomplete list of the class Song, that will return to the 
spotifyAPI and remove the Song ID's of the non-downloaded songs and provide a 
list of which songs were unable to download that way the process can be repeated at a later date 
^^ COMPLETE, TESTED

provide the time the process can be repeated
^^ COMPLETE, TESTED

build the youtube-dl portion (just a playlist download)
^^ INCOMPLETE, DROPPED BECAUSE OF OS FORMATTING ISSUE

increase spotify limit
^^ COMPLETE, TESTED
"""


