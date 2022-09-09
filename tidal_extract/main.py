# Copyright 2022 Wyatt Childers
#
# This file is part of tidal_extract.
#
# tidal_extract is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tidal_extract is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tidal_extract.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import os
import re
import shutil
import tempfile
import zipfile

def parse_args():
  parser = argparse.ArgumentParser(
    description = 'Extract tidal zips into structured folders.'
  )
  parser.add_argument(
    'input_file',
    help = 'file to extract'
  )
  parser.add_argument(
    'music_dir',
    nargs = '?',
    default = None,
    help = 'the path to the user\'s music library'
  )
  parser.add_argument(
    '--verbose',
    dest = 'verbose',
    action = 'store_true',
    help = 'enable verbose mode'
  )

  return parser.parse_args()

TIDAL_ZIP_REGEX = re.compile(r'([A-Za-z ]+)\-([A-Za-z ]+)-FLAC')

def _exit_unknown_zip(reason):
  print(f"This zip is not supported: {reason}.")
  exit(1)

def _verbose_copy2(src_path, dest_path):
  print(f"{src_path} -> {dest_path}")
  shutil.copy2(src_path, dest_path)

def main():
  args = parse_args()

  input_file = os.path.abspath(args.input_file)
  music_dir = args.music_dir if args.music_dir != None else os.getcwd()
  music_dir = os.path.abspath(music_dir)

  copy_fn = _verbose_copy2 if args.verbose else shutil.copy2

  with tempfile.TemporaryDirectory() as tmp_dir:
    with zipfile.ZipFile(input_file, 'r') as zip:
      zip.extractall(tmp_dir)

    dir_contents = os.listdir(tmp_dir)
    if len(dir_contents) != 1:
      _exit_unknown_zip('The zip contains more than one entry.')

    for entry in dir_contents:
      entry_path = os.path.join(tmp_dir, entry)
      if not os.path.isdir(entry_path):
        _exit_unknown_zip('The zip entry isn\'t a directory')

      zip_match = TIDAL_ZIP_REGEX.match(entry)
      if zip_match == None:
        _exit_unknown_zip('The zip doesn\'t match the expected regex')

      artist = zip_match.group(1)
      album = zip_match.group(2)
      album_contents = os.path.join(music_dir, artist, album)
      os.makedirs(album_contents, exist_ok = True)

      shutil.copytree(
        entry_path,
        album_contents,
        copy_function = copy_fn,
        dirs_exist_ok = True
      )
