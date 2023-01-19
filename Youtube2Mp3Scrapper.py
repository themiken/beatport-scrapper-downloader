#!/usr/bin/env python3

__author__ = "Miken"
__version__ = "0.1.0"
__license__ = "MIT"


import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
import youtube_dl
import time


URL = "https://www.beatport.com/genre/hard-techno/2/top-100" # Hard Techno Top 100

def main():
    """ Main entry point of the app """
    print("hello world")

    content = getPage(URL)
    parseContent = parsePage(content)

    # Get songs
    songs = parseContent.find_all("li", class_="bucket-item")

    failedSongs = []


    for song in songs:
        songName  = song.find("span", class_="buk-track-primary-title").text + " - " + song.find("span", class_="buk-track-remixed").text
        print(songName)
        # Search song on youtube
        videosSearch = VideosSearch(songName, limit = 1)
        print("Search: " + songName)

        # Check if song is found
        if videosSearch.result()["result"] != []:
            #Download song
            print(videosSearch.result()["result"][0]["link"])
            downloaded = downloadSong(videosSearch.result()["result"][0]["link"])

            if not downloaded:
                failedSongs.append(songName)
            
        else:
            print("Song not found")

        time.sleep(2)
        

    for song in failedSongs:
        print("Failed to download: {}".format(song))
    
    

def getPage(url):
    print("Getting page: " + url)
    page = requests.get(url)
    return page


def parsePage(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def downloadSong(url):
    try:
        video_info = youtube_dl.YoutubeDL().extract_info(url = url,download=False)
        filename = f"{video_info['title']}.mp3"
        options={
            'format':'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }


        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        print("Download complete... {}".format(filename))
        return True
    except Exception as e:
        print("Error: {}".format(e))
        return False



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
