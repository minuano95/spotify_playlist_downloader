# ---------------------------------------
# download youtube content improts
from moviepy.editor import VideoFileClip
from pytube import YouTube
from pytube.cli import on_progress
# ---------------------------------------

from bs4 import BeautifulSoup
from time import sleep
import threading
import requests
import json
import pprint
import os
import re


# https://developer.spotify.com/console/get-playlist/?playlist_id=1s9MirMoT3CDgBNGgMcECL&market=&fields=&additional_types= 


TOKEN = input('Spotify Token: ')
PATH = input('Path: ').replace('/', '\\')
PLAYLIST_ID = input('Playlist ID: ')

songs = []

BASE_URL = 'https://api.spotify.com/v1/'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}'}

def get_response(query):
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS)
    print_response = json.dumps(response.json(), indent=2)
    print_response2 = json.loads(print_response)
    return print_response2


# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def get_playlist_songs(playlist_id):
    
    playlist_data = get_response(f'playlists/{playlist_id}')
    for song in playlist_data['tracks']['items']:
        
        song_name = song['track']['name']
        
        # Getting the artists names
        artists = []
        for artist in song['track']['artists']:
            artists.append(artist['name'])

        artist = ', '.join(letra for letra in artists)
        songs.append(song_name + ' ' + artist)


# ------------------------------------

def download_video(link):
    yt = YouTube(link, on_progress_callback=on_progress)
    video_title = yt.title
    video_title = [letra for letra in video_title if letra not in '''./$,~´`:*?"'><|''']
    video_title = ''.join(video_title)
    print('Video:', yt.title)
    print('Downloading...')
    
    video = yt.streams.get_by_resolution('360p')
    video.download(output_path=PATH ,filename=video_title + '.mp4')
    
    return video_title


def youtube_content_dowloader(link):
    
    print('Converting...')

    # Formating the filename and downloading the video
    filename = download_video(link)

    # defining the mp3 and mp4 filenames
    mp4_file = rf"{PATH}\{filename}.mp4"
    mp3_file = rf'{PATH}\{filename}.mp3'

    # Converting
    video_clip = VideoFileClip(mp4_file)
    
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3_file)
    
    audio_clip.close()
    video_clip.close()

    # deleting the mp4 file
    os.remove(mp4_file)


def get_youtube_urls(search_term):
    if search_term not in songs_scraped:
        songs_scraped.append(search_term)

        req = requests.get(f'https://www.youtube.com/results?search_query={search_term.replace(" ", "+")}')
        soup = BeautifulSoup(req.text, 'html.parser')

        for child in soup.find_all('script')[33].children:
            json_data = child[21:-1]
        
        url = re.findall(r'/watch\?v=.{11}', json_data)

        songs_urls.append(url[0])


get_playlist_songs(PLAYLIST_ID)

songs_scraped = []
songs_urls = []

for song in songs:
    x = threading.Thread(target=get_youtube_urls, args=(song,))
    x.start()
    while threading.active_count() >= 5:
        sleep(0.5)

sleep(2)
print(len(songs_urls))

for song_url in songs_urls:
    while True:
        try:    
            x = threading.Thread(target=youtube_content_dowloader, args=(song_url,))
            x.start()
            while threading.active_count() >= 10:
                sleep(1)
            break
        except Exception as e:
            print('Ocorreu um erro ao baixar a música:', song_url)
