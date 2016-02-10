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

import pickle
import csv
import sys

from commit import Commit
from tokenize_commit import tokenize
from datetime import datetime

# Extend the limit of a single line.
csv.field_size_limit(2**31)


def unescape_message(text):
    return text\
        .replace('\\n', '\n')\
        .replace('\\r', '\r')\
        .replace('\\\\', '\\')

filename = sys.argv[1]
commits = []


with open(filename, encoding='UTF-8') as csv_file:
    reader = csv.reader(csv_file, quoting=csv.QUOTE_ALL)

    for row in reader:
        try:
            repo, sha, time_str, message_raw, status = row
        except ValueError as e:
            from pprint import pprint as print
            print(row)
            raise e

        time = datetime.fromtimestamp(int(time_str) // 10**6)
        message = unescape_message(message_raw)
        tokens = tokenize(message)

        commit = Commit(repo=repo, sha=sha, time=time, message=message,
                        tokens=tokens, status=status)
        if not commit.is_merge:
            commits.append(commit)

with open('commits.pickle', 'wb') as pickle_file:
    pickle.dump(commits, pickle_file)
