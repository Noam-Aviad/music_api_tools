# music_api_tools

## Requirements:
spotipy

lyricsgenius

## Description:

This module uses the spotipy and lyricsgenius libaries to provide a simple way to gather data from the Spotify and Genius API's, and to modify Spotify playlists.
The module has different classes to handle songs, albums and artists as demonstrated below.

### class Song:

#### Attributes:

**spot** - a Spot object (explained below)

**title** - string of the song title

**spotify_id** - Spotify ID (string)

**genius_id** - Genius ID (int)

**spotify_data** - song data from Spotify (dict)

**genius_data** - song data from Genius (dict)

**album** - Album object

**artist** - artist object

**lyrics** - song lyrics (string). Only initiallized after calling the lyrics() method.

**word_frequencies** - words from the song and each word's frequency (dict). Only initiallized after calling the word_frequencies() method.

#### Methods:

**lyrics(tidy_up (bool))** - returns song lyrics (string) and stores them as an attribute. tidy_up cleans up the lyrics from extra text (e.g: "[Verse 1]", "Pre-chorus" etc.).

**words_count(only_unique (bool))** - returns the amount of words in the song (int). if only_unique it doesn't count word repetitions.

**genius_annotations()** - returns Genius annotations for the lyrics (list).

**word_frequencies(caps_sensitive (bool))** - returns (and stores as attribute) the frequencies of each word in the song (dict).

### class Album:

#### Attributes:

**spot** - a Spot object (explained below)

**title** - string of the album title

**spotify_id** - Spotify ID (string)

**genius_id** - Genius ID (int)

**spotify_data** - album data from Spotify (dict)

**genius_data** - album data from Genius (dict)

**songs** - list of Song objects of the album's tracks. Only initiallized after calling the songs() method.

**artist** - artist object

**words** - list of words from the album's songs. Only initiallized after calling the words() method.

**word_frequencies** - words from the album's songs and each word's frequency (dict). Only initiallized after calling the word_frequencies() method.

#### Methods:

**words(only_unique (bool))** - returns list of words in the album and stores them as an attribute.

**words_count(only_unique (bool))** - returns the amount of words in the album (int). if only_unique it doesn't count word repetitions.

**word_frequencies(caps_sensitive (bool))** - returns (and stores as attribute) the frequencies of each word in the album (dict).

### class Artist:

#### Attributes:

**spot** - a Spot object (explained below)

**name** - string of the artist's name

**spotify_id** - Spotify ID (string)

**genius_id** - Genius ID (int)

**spotify_data** - artist data from Spotify (dict)

**genius_data** - artist data from Genius (dict)

**songs** - list of Song objects by the artist. Only initiallized after calling the songs() method.

**albums** - list of Album objects by the artist. Only initiallized after calling the albums() method.

**words** - list of words from the artist's songs. Only initiallized after calling the words() method.

**word_frequencies** - words from the artistm's songs and each word's frequency (dict). Only initiallized after calling the word_frequencies() method.

#### Methods:

**words(only_unique (bool))** - returns list of words in the artist's songs and stores them as an attribute.

**words_count(only_unique (bool))** - returns the amount of words in the artist's songs (int). if only_unique it doesn't count word repetitions.

**word_frequencies(caps_sensitive (bool))** - returns (and stores as attribute) the frequencies of each word in the artist's songs (dict).


