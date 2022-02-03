# **SpotPlay2YouPlay**

######*Converts new additions to a Spotify playlist to a matching Youtube playlist, can also be configured to converting whole playlists with the refresh function. Requires 3 youtube/google credentials to operate at full capacity, and needs 1 spotify api *

## **HOW TO USE DETAILED IN STEPS IN THE DIRECTIONS.TXT FILE**

I built my first messy but functional Python script that converts a Spotify playlist to a YouTube playlist, while storing the song IDs locally to avoid adding the same songs twice. The default is that every time the program is run, the YouTube playlist is cleared and only the new songs are added, but this can be controlled by calling a function called refresh. You can imagine the uses, and any advice would be greatly appreciated!

As for the workings, here's the breakdown in steps:
1. It asks the user for a Spotify playlist
2. The user inputs the "share this playlist" link
3. The program will fetch all the songs in the playlist and simplify the info to their unique ID, artist names and song name. (The Spotify song object is LOADED with useless info for this application)
4. The program creates a file called Depot.txt (if it's not already present) and stores in every new unique song ID, checking the Depot file every time to ensure the ID isn't already there to avoid repeated Spotify songs. (The song ID is still unique even if it's found in different playlists)
5. The known songs get ignored, and the new songs get added to a list variable called 'queue'. (To avoid songs from getting ignored, you can uncomment the refresh() function in the main code page - refresh() just deletes the Depot.txt file every time it starts)
6. The YouTubeAPI kicks in its first function and starts deleting all the songs on the YouTube playlist using the API functions list and delete, doing this by video ID to save usage points (so you don't DL them twice) but this function can also be removed by just commenting out any instance of the delete_ all_in_playlist() function on the main page and the structural code around them.  
7. With a fresh and empty YouTube playlist, the previously mentioned queue variable filled with the new songs will use the YouTubeAPI to search the first instance of that song using the song title and artists. It will then add that song to the YouTube playlist immediately. 
8. YoutubeAPI's have a ridiculously small daily use limit, which is why it switches between 3 pages of credentials. It has a total capacity of around 200 delete and add operations. When an API reaches its limit, it will catch the server error and swap to another API after removing every song that didn't download from Depot (so that it's considered a new song again) To remove these songs it will use the Song_Removal() function.
9. If the total capacity of all three of the YouTubeAPI is met, it will remove the unadded songs from Depot for the last time and show the time (in EST) and date that the process can be repeated. (Keep in mind the same playlist can be reused and only the missed songs will be added.
10. If the total capacity isn't met, then the program will just stop without error and the YouTube playlist will be filled with the playlists' songs.
I might've missed small details so be sure to keep looking through the code comments at the top of the pages and throughout to fully grasp the idea
