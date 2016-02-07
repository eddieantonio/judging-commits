#!/usr/bin/env python3
# coding: UTF-8

# Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import sys

from pymongo import MongoClient
from tqdm import tqdm

GH_TORRENT_URL = 'mongodb://ghtorrentro:ghtorrentro@localhost/github'
csv_filename = sys.argv[1]


def should_exclude(db, repo, sha, *_):
    # Find the commit, regardless of the number of parents it has.
    commit = db.commits.find_one({
        'sha': sha,
    }, {'url': 1, 'parents': 1,  '_id': 0})

    if commit is None:
        # Commit not found!
        return True

    if len(commit['parents']) > 1:
        assert repo in commit['url'], 'Improbably, the SHA collided'
        # Commit is a merge!
        return True

    return False


with open('non-merge-commits.csv', 'w') as outfile,\
        open(csv_filename, 'r') as csv_file,\
        MongoClient(GH_TORRENT_URL) as mongo:
    output = csv.writer(outfile)
    for row in tqdm(csv.reader(csv_file)):
        if should_exclude(mongo.github, *row):
            continue
        # Copy the row over.
        output.writerow(row)
