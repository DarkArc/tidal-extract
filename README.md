# tidal-extract

A simple tool for extracting a zip file downloaded from http://store.tidal.com
converting as part of the extraction process names like `Artist-Album
Name-FLAC/` into `$music_dir/Artist/Album Name/`.

```
usage: tidal-extract [-h] [--verbose] input_file [music_dir]

Extract tidal zips into structured folders.

positional arguments:
  input_file  file to extract
  music_dir   the path to the user's music library

options:
  -h, --help  show this help message and exit
  --verbose   enable verbose mode
```
