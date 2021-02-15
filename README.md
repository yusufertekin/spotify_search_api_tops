# Spotify SEARCH API Experimental Usage - NOT PRODUCTION READY ONLY FOR DEVELOPMENT

This project aims to use Spotify Search API to fetch 50 tracks of artist randomly chosed from given file.  

Have a single web-service named “ tracks “ This HTTP service will accept a
music genre type as input and do the following:
1. Pick a random artist associated to that genre from " genres.json " file, which will be provided
by us.
2. Filter the most popular 10 tracks (songs) of that artist from the first 50 tracks obtained from
Spotify Search API (eg. "rock" genre will retrieve the most popular 10 track info of "Led
Zeppelin", which is randomly chosen).

This doesn't use any database. Instead it keeps artist list of each genre in cache. 
Once a request made for a genre, result of randomly chosen artist is cached for 5 mins.

# How to run
1. Create a .env file and place it on root of the project (same directory with docker-compose.yml)
  * .env file must contain two env vars
    * SPOTIFY_API_CLIENT_ID
    * SPOTIFY_API_CLIENT_SECRET
 
2. Place genres.json file under "alotech/static/data/" directory

3. Run docker-compose build

4. Run docker-compose run

# Configurations
* NUM_OF_TRACKS_TO_BE_FETCHED = 50
* NUM_OF_TOP_TRACKS = 10
* TRACKS_CACHE_TIMEOUT = 300 # 5 MINS

# Developer Notes
1. urllib is used to eliminate the need of external library. However, for ease use I'd prefer using requests library.
2. This project contains single endpoint if it needs to be expanded, I'd use django rest framework
3. There is only single page, if there were more, I'd rather using Vuejs to build frontend instead of pure javascript. 
4. If this was not for experimental purposes, I'd directly use Spotify Artist API to fetch top tracks of an artist
