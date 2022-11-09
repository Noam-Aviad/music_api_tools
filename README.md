# music_api_tools

## Description:

This module uses the spotipy and lyricsgenius libraries to provide a simple way to gather data from the Spotify and Genius API's, and to modify Spotify playlists.
The module has different classes to handle songs, albums and artists as demonstrated below.

## Requirements:
spotipy

lyricsgenius

Get the API keys (as explained in these links: [Spotify](https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b) and [Genius](https://melaniewalsh.github.io/Intro-Cultural-Analytics/04-Data-Collection/07-Genius-API.html)) and place them in the keys.txt file.


## Examples:
Initializing a Song object:
````
import music_api_tools as mt
werewolves_of_london = mt.Song(title = 'Werewolves of London')
````

input:
````
print(werewolves_of_london.artist.name)
````
output:
````
Warren Zevon
````
input:
````
print(werewolves_of_london.album.title)
````
output:
````
Excitable Boy
````
input:
````
print(werewolves_of_london.album.spotify_data)
````
output:
````
{'album_type': 'album', 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/3mY9Ii0cL5SQxpOTAm8SHx'}, ...
````
input:
````
print(werewolves_of_london.genius_data)
````
output:
````
{'song': {'annotation_count': 22, 'api_path': '/songs/72605', 'apple_music_id': '1048476311', ...
````
input:
````
print(werewolves_of_london.artist.word_frequencies())
````
output:
````
{'well,': 195, "i'm": 663, 'gone': 28, 'to': 1501, 'detox': 16, 'mansion': 17, 'way': 94, 'down': 517, 'on': 890, 'last': 46, ...
````

### class Spot: 
This class mainly passes data from spotipy to the other classes. 

It also has the ````merge_playlists(new_playlist (str), playlists(list of strings), remove_duplicates (bool))```` method which  accepts the ID's of your Spotify playlists and creates a new playlist with all the content from your other playlists.

*If you don't specify any playlists, by default it will use all of your playlists.

*This method can't merge playlists with local files.

### class Song:
Accepts one of the following to initialize: title and optionally artist_name (strings), genius_id (int) or spotify_id (string).

#### Attributes:

**spot** - a Spot object (explained below)

**title** - string of the song title

**spotify_id** - Spotify ID (string)

**genius_id** - Genius ID (int)

**spotify_data** - song data from Spotify (dict)

**genius_data** - song data from Genius (dict)

**album** - Album object

**artist** - artist object

**lyrics** - song lyrics (string). Only initialized after calling the lyrics() method.

**word_frequencies** - words from the song and each word's frequency (dict). Only initialized after calling the word_frequencies() method.

#### Methods:

**lyrics(tidy_up (bool))** - returns song lyrics (string) and stores them as an attribute. tidy_up cleans up the lyrics from extra text (e.g: "[Verse 1]", "Pre-chorus" etc.).

**words_count(only_unique (bool))** - returns the amount of words in the song (int). if only_unique it doesn't count word repetitions.

**genius_annotations()** - returns Genius annotations for the lyrics (list).

**word_frequencies(caps_sensitive (bool))** - returns (and stores as attribute) the frequencies of each word in the song (dict).

### class Album:
Accepts one of the following to initialize: title and optionally artist_name (strings), genius_id (int) or spotify_id (string).

#### Attributes:

**spot** - a Spot object (explained below)

**title** - string of the album title

**spotify_id** - Spotify ID (string)

**genius_id** - Genius ID (int)

**spotify_data** - album data from Spotify (dict)

**genius_data** - album data from Genius (dict)

**songs** - list of Song objects of the album's tracks. Only initialized after calling the songs() method.

**artist** - artist object

**words** - list of words from the album's songs. Only initiallized after calling the words() method.

**word_frequencies** - words from the album's songs and each word's frequency (dict). Only initialized after calling the word_frequencies() method.

#### Methods:

**words(only_unique (bool))** - returns list of words in the album and stores them as an attribute.

**words_count(only_unique (bool))** - returns the amount of words in the album (int). if only_unique it doesn't count word repetitions.

**word_frequencies(caps_sensitive (bool))** - returns (and stores as attribute) the frequencies of each word in the album (dict).

### class Artist:
Accepts one of the following to initialize: name (string), genius_id (int) or spotify_id (string).

#### Attributes:

**spot** - a Spot object (explained below)

**name** - string of the artist's name

**spotify_id** - Spotify ID (string)

**genius_id** - Genius ID (int)

**spotify_data** - artist data from Spotify (dict)

**genius_data** - artist data from Genius (dict)

**songs** - list of Song objects by the artist. Only initialized after calling the songs() method.

**albums** - list of Album objects by the artist. Only initialized after calling the albums() method.

**words** - list of words from the artist's songs. Only initialized after calling the words() method.

**word_frequencies** - words from the artistm's songs and each word's frequency (dict). Only initialized after calling the word_frequencies() method.

#### Methods:

**words(only_unique (bool))** - returns list of words in the artist's songs and stores them as an attribute.

**words_count(only_unique (bool))** - returns the amount of words in the artist's songs (int). if only_unique it doesn't count word repetitions.

**word_frequencies(caps_sensitive (bool))** - returns (and stores as attribute) the frequencies of each word in the artist's songs (dict).


