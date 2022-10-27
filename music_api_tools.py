import spotipy
import json
import lyricsgenius as lg
import re

class Spot:
    def __init__(self):
        with open('keys.txt') as keys:
            keys = json.loads(keys.read())
            self.cid = keys['Spotify client id']
            self.secret = keys['Spotify client secret']
            self.scope = keys['Spotify scope']
            self.redirect = keys['Spotify redirect']
        self.spotipy = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id=self.cid, client_secret=self.secret, redirect_uri=self.redirect, scope=self.scope))

    def all_user_playlists(self):
        sp = self.spotipy
        next_playlists = sp.current_user_playlists()
        playlists = next_playlists['items']
        while next_playlists['next']:
            next_playlists = sp.next(next_playlists)
            playlists.extend(next_playlists['items'])
        for i in range(len(playlists)):
            playlists[i] = playlists[i]['id']
        return playlists

    def playlist_all_items(self, playlist_id, remove_duplicates=False):
        sp = self.spotipy
        next_tracks = sp.playlist_items(playlist_id)   #first ones aren't just IDs
        tracks = []
        for i in next_tracks['items']:
            if i['track']:
                tracks.append(i['track']['id'])
        while next_tracks['next']:
            next_tracks = sp.next(next_tracks)
            for i in next_tracks['items']:
                if i['track']['id']:
                    tracks.append(i['track']['id'])
        if remove_duplicates:
            tracks = [*set(tracks)]
        return tracks

    def user_all_tracks(self):
        user_playlists = self.all_user_playlists()
        tracks = []
        for i in user_playlists:
            tracks.extend(self.playlist_all_items(i))
        return list(set(tracks))

    def merge_playlists(self,  new_playlist, playlists=None, remove_duplicates=True, description = None, collaborative=False, public = False):
        sp = self.spotipy
        if playlists==None:
            playlists = self.all_user_playlists()
        tracks = []
        for i in playlists:
            tracks.extend((self.playlist_all_items(i)))
        sp.user_playlist_create(user = sp.current_user()['id'], name = new_playlist, public=public, collaborative=collaborative, description=description)
        if remove_duplicates:
            tracks = [*set(tracks)]
        tracks = split_to_chunks(tracks)
        for i in tracks:
            sp.playlist_add_items(self.all_user_playlists()[0], i)
        return

class Song:
    def __init__(self, title=None, artist_name=None, spotify_id=None, genius_id=None, album = None, artist = None):
        self.spot = Spot()
        with open('keys.txt') as keys:
            keys = json.loads(keys.read())
        self.genius = lg.Genius(keys['Genius token'])
        if album:
            self.album = album
        if artist:
            self.artist = artist
        if title:
            self.title = title
            if artist_name and not artist:
                search_term = title + artist_name
                self.artist = Artist(name=artist_name)
            else:
                search_term = title
            try:
                self.genius_id = self.genius.search(search_term=search_term, type_='song')['sections'][0]['hits'][0]['result']['id']
                self.genius_data = self.genius.song(song_id=self.genius_id)
            except:
                pass
            if artist_name == None and artist==None:
                self.artist = Artist(name=self.genius_data['song']['artist_names'])
            if album==None:
                try:
                    self.album = self.genius_data['song']['album']['full_title']
                    self.album = Album(title=self.album.removesuffix((" by " + self.artist.name)))
                except:
                    pass
            self.spotify_id = self.spot.spotipy.search(q=search_term, limit=1, type='track')['tracks']['items'][0]['id']
        elif genius_id:
            self.genius_id = genius_id
            try:
                self.genius_data = self.genius.song(song_id=genius_id)
                self.title = self.genius_data['song']['title']
                if artist==None:
                    self.artist = Artist(name=self.genius_data['song']['artist_names'])
                if album==None:
                    self.album = self.genius_data['song']['album']['full_title']
                    self.album = Album(title=self.album.removesuffix((" by " + self.artist.name)))
            except:
                pass
            try:
                self.spotify_id = self.spot.spotipy.search(q=(self.title + self.artist.name), limit=1)['tracks']['items'][0]['id']
                self.spotify_data = self.spot.spotipy.track(self.spotify_id)
            except:
                pass
        elif spotify_id:
            self.spotify_data = self.spot.spotipy.track(spotify_id)
            self.title = self.spotify_data['name']
            if artist==None:
                self.artist = Artist(name=self.spotify_data['artists'][0]['name'])
            if album==None:
                self.album = Album(title=self.spotify_data['album']['name'])

    def lyrics(self, tidy_up = True):
        lyrics = self.genius.lyrics(self.genius_id)
        if tidy_up:
            lyrics = lyrics.removeprefix(self.title + " Lyrics")
            lyrics = re.sub(r'\[[A-Za-z \s 0-9]+\]', '', lyrics)
            lyrics = re.sub(r'[0-9]+Embed', '', lyrics)
        return lyrics

    def words_count(self, only_unique = False):
        lyrics = self.lyrics(tidy_up=True).split()
        if only_unique:
            lyrics = [*set(lyrics)]
        return len(lyrics)

    def genius_annotations(self):
        return self.genius.song_annotations(self.genius_id)

    def word_frequencies(self, caps_sensitive = False):
        words = self.lyrics(tidy_up=True).split()
        word_frequencies = {}
        for word in words:
            if not caps_sensitive:
                word = word.lower()
            if word in word_frequencies:
                word_frequencies[word] += 1
            else:
                word_frequencies[word] = 1
        return word_frequencies

class Album:
    def __init__(self, title = None, artist_name = None, spotify_id = None, genius_id = None, artist = None):
        self.sp = Spot()
        with open('keys.txt') as keys:
            keys = json.loads(keys.read())
        self.genius = lg.Genius(keys['Genius token'])
        if artist:
            self.artist = artist
        if title:
            self.title = title
            if artist_name and not artist:
                self.artist = Artist(name=artist_name)
                search_term = title + artist_name
            else:
                search_term = title
            result = self.genius.search(search_term, type_='album', per_page=1)
            # try:
            self.genius_id = result['sections'][0]['hits'][0]['result']['id']
            self.genius_data = self.genius.album(self.genius_id)
            self.artist = Artist(genius_id=self.genius_data['album']['artist']['id'])
            # except:
            #     pass
            try:
                self.spotify_id = self.sp.spotipy.search(q = search_term, limit=1, type='album')['albums']['items'][0]['id']
                self.spotify_data = self.sp.spotipy.album(self.spotify_id)
            except:
                pass
        elif genius_id:
            self.genius_id = genius_id
            self.genius_data = self.genius.album(genius_id)
            full_title = (self.genius_data['album']['full_title']).split(" by ")
            self.title = full_title[0]
            if artist==None:
                self.artist = Artist(name=full_title[1])
            search_term = self.title + self.artist.name
            try:
                self.spotify_id = self.sp.spotipy.search(q=search_term, limit=1, type='album')['albums']['items'][0]['id']
                self.spotify_data = self.sp.spotipy.album(self.spotify_id)
            except:
                pass
        elif spotify_id:
            self.spotify_id = spotify_id
            self.spotify_data = self.sp.spotipy.album(spotify_id)
            self.title = self.spotify_data['name']
            if artist==None:
                self.artist = Artist(name=self.spotify_data['artists'][0]['name'])
            search_term = self.title + self.artist
            result = self.genius.search(search_term, type_='album', per_page=1)
            self.genius_id = result['sections'][0]['hits'][0]['result']['id']
            self.genius_data = self.genius.album(self.genius_id)

    def songs(self, print_progress = True):
        songs = []
        tracks_list = self.genius.album_tracks(self.genius_id)['tracks']
        i=0
        for track in tracks_list:
            if print_progress:
                print(f"Creating Song object for: '{track['song']['title']}'")
            songs.append(Song(genius_id=track['song']['id'], album=self, artist=self.artist))
            i+=1
            if print_progress:
                print(f"Created Song objects for {i} out of {len(tracks_list)} songs in '{self.title}'")
        self.songs = songs
        return self.songs

    def words(self, only_unique = False, print_progress = True):
        if self.songs and isinstance(self.songs, list):
            songs = self.songs
        else:
            songs = self.songs(print_progress=print_progress)
        words = []
        i=0
        try:
            for song in songs:
                words.extend(song.lyrics(tidy_up=True).split())
                i+=1
                if print_progress:
                    print(f"Fetched lyrics for {i} out of {len(songs)} songs in '{self.title}'")
            if only_unique:
                words = [*set(words)]
            self.words = words
            return self.words
        except:
            return

    def words_count(self, only_unique = False):
        self.words_count =len(self.words(onlyUnique=only_unique))
        return self.words_count

    def word_frequencies(self, caps_sensitive = False, print_progress = True):
        if self.words and isinstance(self.words, list):
            words = self.words
        else:
            words = self.words(only_unique=False, print_progress=print_progress)
        word_frequencies = {}
        for word in words:
            if not caps_sensitive:
                word = word.lower()
            if word in word_frequencies:
                word_frequencies[word] += 1
            else:
                word_frequencies[word] = 1
        self.word_frequencies = word_frequencies
        return self.word_frequencies

class Artist:
    def __init__(self, name=None, genius_id=None, spotify_id=None):
        self.sp = Spot()
        with open('keys.txt') as keys:
            keys = json.loads(keys.read())
        self.genius = lg.Genius(keys['Genius token'])
        if name:
            self.name = name
            result = self.genius.search(search_term=name, per_page=1, type_='artist')
            try:
                self.genius_id = result['sections'][0]['hits'][0]['result']['id']
                self.genius_data = self.genius.artist(self.genius_id)
            except:
                pass
            try:
                self.spotify_id = self.sp.spotipy.search(q=name, limit=1, type='artist')['artists']['items'][0]['id']
                self.spotify_data = self.sp.spotipy.artist(self.spotify_id)
            except:
                pass
        elif genius_id:
            self.genius_id = genius_id
            self.genius_data = self.genius.artist(genius_id)
            self.name = self.genius_data['artist']['name']
            self.spotify_id = self.sp.spotipy.search(q=self.name, limit=1, type='artist')['artists']['items'][0]['id']
            self.spotify_data = self.sp.spotipy.artist(self.spotify_id)
        elif spotify_id:
            self.spotify_id = spotify_id
            self.spotify_data = self.sp.spotipy.artist(spotify_id)
            self.name = self.spotify_data['name']
            result = self.genius.search(search_term=self.name, per_page=1, type_='artist')
            self.genius_id = result['sections'][0]['hits'][0]['result']['id']
            self.genius_data = self.genius.artist(self.genius_id)

    def albums(self, print_progress = True):
        album_list = self.genius.artist_albums(self.genius_id)['albums']
        albums = []
        for album in album_list:
            if print_progress:
                print('Creating Album object for: ', album['full_title'])
            albums.append(Album(genius_id=album['id'], artist=self))
        self.albums = albums
        return self.albums

    def songs(self, print_progress = True):
        if self.albums and isinstance(self.albums, list):
            albums = self.albums
        else:
            albums = self.albums(print_progress=print_progress)
        songs = []
        i=0
        for album in albums:
            songs.extend(album.songs())
            i+=1
            if print_progress:
                print(f"Created Song objects for {i} out of {len(albums)} albums")
        self.songs = songs
        return self.songs

    def words(self, only_unique=False, print_progress=True):
        words = []
        album_list = self.albums(print_progress=print_progress)
        i=0
        for album in album_list:
            if print_progress:
                print(f"Creating Song objects for album: '{album.title}' by '{album.artist.name}'")
            try:
                words.extend(album.words(print_progress=print_progress))
                i+=1
                if print_progress:
                    print(f"Fetched lyrics for {i} out of {len(album_list)} albums by {self.name}")
            except:
                pass
        if only_unique:
            words = [*set(words)]
        self.words = words
        return self.words

    def word_frequencies(self, caps_sensitive = False, print_progress=True): # returns and sets self.wordFrequencies to a dict where the keys are all the words in the artist's songs and the values are each word's frequency
        if self.words and isinstance(self.words, list):
            words = self.words
        else:
            words = self.words(only_unique=False, print_progress=print_progress)
        word_frequencies = {}
        for word in words:
            if not caps_sensitive:
                word = word.lower()
            if word in word_frequencies:
                word_frequencies[word] += 1
            else:
                word_frequencies[word] = 1
        self.word_frequencies = word_frequencies
        return self.word_frequencies

def split_to_chunks(items, n=100):  # a function that splits lists of tracks to handle Spotify's API limit on adding tracks to playlists
    length = len(items)
    chunks = []
    for i in range(0,length,n):
        k = min(n, length-i)
        chunks.append(items[i:i+k])
    return chunks