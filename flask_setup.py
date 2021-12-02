from main import scraping_and_downloading_songs
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        playlist_id = request.form['playlist_id']
        token = request.form['token']
        download_path = request.form['download_path']

        global songs_names_and_artists
        songs, songs_names_and_artists = scraping_and_downloading_songs(playlist_id, token, download_path)

        return redirect(url_for('songs'))
    
    else:
        return render_template('index.html')


@app.route('/songs')
def songs():

    print()
    print('-'*40)

    for song in songs_names_and_artists:
            print(song)
    print('Length songs:', len(songs_names_and_artists))

    return render_template('songs.html', songs_names_and_artists=songs_names_and_artists)

app.run(debug=True)