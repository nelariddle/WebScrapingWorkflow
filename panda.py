import pandas as pd

# Simple code for the use-case of grabbing a table
# Returns a list of all tables on the site, so we index with [0] to get the first one
pd.read_html("https://en.wikipedia.org/wiki/List_of_Spotify_streaming_records")[0]
