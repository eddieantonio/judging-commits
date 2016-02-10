#!/usr/bin/env python
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

_, status_filename, commits_filename = sys.argv

statuses = {}

with open(status_filename, encoding='UTF-8') as status_file:
    for repo, sha, status in csv.reader(status_file):
        statuses[(repo, sha)] = status

# Extend the limit of a single line.
csv.field_size_limit(2**31)

with open(commits_filename, encoding='UTF-8') as commit_file,\
        open('commits-combined.csv', 'w', encoding='UTF-8') as out_file:
    output = csv.writer(out_file, quoting=csv.QUOTE_ALL)
    for row in csv.reader(commit_file):
        repo, sha, *_ = row

        try:
            status = statuses[(repo, sha)]
        except KeyError:
            continue

        output.writerow(tuple(row) + (status,))
