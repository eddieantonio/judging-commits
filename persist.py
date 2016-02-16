#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

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

import itertools
import os
import re
import sqlite3
from datetime import datetime
from itertools import repeat

from tqdm import tqdm

from commit import Commit


SCHEMA = """\
-- Original data from Boa
CREATE TABLE IF NOT EXISTS
commits_raw (
    repo    TEXT NOT NULL,
    sha     TEXT NOT NULL,

    -- Commit creation date.
    time    DATE NOT NULL,
    message TEXT NOT NULL,

    PRIMARY KEY (repo, sha)
);


-- Travis-CI
CREATE TABLE IF NOT EXISTS
status_check (
    repo    TEXT NOT NULL,
    sha     TEXT NOT NULL,

    -- Insertion date.
    time    DATE NOT NULL
            DEFAULT CURRENT_TIMESTAMP,

    -- The actual status!
    status  TEXT NOT NULL,

    PRIMARY KEY (repo, sha)
);


-- Leave-one-out perplexity
CREATE TABLE IF NOT EXISTS
perplexity (
    repo    TEXT NOT NULL,
    sha     TEXT NOT NULL,

    -- Insertion date.
    time    DATE NOT NULL
            DEFAULT CURRENT_TIMESTAMP,

    -- The actual perplexity!
    perplexity  REAL NOT NULL,

    PRIMARY KEY (repo, sha)
);


CREATE VIEW IF NOT EXISTS commits
AS SELECT
    c.repo AS repo,
    c.sha AS sha,
    c.time AS time,
    c.message AS message,
    status,
    perplexity
FROM
    commits_raw AS c
    JOIN status_check   USING (repo, sha)
    JOIN perplexity     USING (repo, sha)
WHERE
    status IS NOT 'cancelled';


CREATE VIEW IF NOT EXISTS repositories
AS SELECT DISTINCT
    repo AS name,
    COUNT(sha) as commits
FROM commits;


-- Look-up a commit by SHA; since there may be
-- forks, there are probably duplicates.
CREATE INDEX IF NOT EXISTS
commit_sha ON commits_raw (sha);
"""

FILENAME = os.getenv('COMMIT_DATABASE',
                     os.path.join(os.path.dirname(__file__),
                                  'commits.sqlite'))

# Connect initially, and create the schema.
conn = sqlite3.connect(FILENAME)
conn.executescript(SCHEMA)


def insert_commit(repo, sha, time, message):
    """
    Persist  a raw commit from Boa.
    """
    assert '/' in repo, 'Invalid repository name: %r' % (repo,)
    assert re.match(r'[a-f0-9]{40}', sha), 'Invalid SHA: %r' % (sha, )
    assert isinstance(time, datetime), 'Not a valid datetime: %r' % (time,)
    assert message is not None

    with conn:
        conn.execute('''\
            INSERT INTO commits_raw (
                repo, sha, time, message
            ) VALUES (?, ?, ?, ?)
        ''', (repo, sha, time, message))


def fetch_commit(repo=None, sha=None):
    """
    Fetch a single commit by its repository name and SHA, or simply its SHA.
    """
    if not repo and not sha:
        raise ValueError('Must provide either repo or sha')
    if not repo:
        return fetch_commit_by_sha(sha)

    cursor = conn.execute('''
        SELECT
            repo, sha, time, message, status, perplexity
        FROM commits
        WHERE
            repo = ? AND
            sha = ?
    ''', (repo, sha))

    try:
        return Commit(*cursor.fetchone())
    except TypeError:
        raise KeyError(sha)


def fetch_commit_by_sha(sha):
    cursor = conn.execute('''
        SELECT
            repo, sha, time, message, status, perplexity
        FROM commits
        WHERE
            sha = ?
    ''', (sha,))

    try:
        return Commit(*cursor.fetchone())
    except TypeError:
        raise KeyError(sha)


def insert_status(repo, sha, status):
    """
    Persist a build status.
    """

    with conn:
        conn.execute('''\
            INSERT INTO status_check (
                repo, sha, status
            ) VALUES (?, ?, ?)
        ''', (repo, sha, status))


def insert_perplexity(repo, sha, perplexity):
    """
    Persist perplexity.  You must manually calculate cross-entropy when
    retrieving these values.
    """

    with conn:
        conn.execute('''\
            INSERT INTO perplexity (
                repo, sha, perplexity
            ) VALUES (?, ?, ?)
        ''', (repo, sha, perplexity))


def unescape_message(text):
    return text\
        .replace('\\n', '\n')\
        .replace('\\r', '\r')\
        .replace('\\\\', '\\')


def insert_commits_raw(repo, sha, time_str, message):
    time = datetime.fromtimestamp(int(time_str) // 10**6)
    return insert_commit(repo,
                         sha,
                         time,
                         unescape_message(message))


def fetch_raw_commits(exclude_repositories=()):
    """
    Yields all commits, with status and perplexity set to null.
    """

    query = r'''
        SELECT repo, sha, time, message
        FROM commits_raw
    '''

    if exclude_repositories:
        # Convert string to single value tuple.
        if isinstance(exclude_repositories, str):
            exclude_repositories = (exclude_repositories,)
        placeholders = ', '.join(repeat('?', len(exclude_repositories)))
        query = '''
            {query}
            WHERE repo NOT IN ({placeholders})
        '''.format(query=query,
                   placeholders=placeholders)

    for row in conn.execute(query, exclude_repositories):
        yield Commit(repo=row[0], sha=row[1], time=row[2], message=row[3],
                     status=None, perplexity=None)


def fetch_commits():
    """
    Yields all fully-processed commits.
    """

    cursor = conn.execute(r'''
        SELECT
            repo, sha, time, message, status, perplexity
        FROM commits
    ''')

    for row in cursor:
        yield Commit(*row)


def do_insert_from_csv(insert, filename):
    import csv
    csv.field_size_limit(2**31)

    with open(filename, 'r', encoding="UTF=8") as commits_file:
        for row in tqdm(csv.reader(commits_file)):
            insert(*row)


if __name__ == '__main__':
    import sys

    _, mode, argument = sys.argv
    insert = None
    lookup = None

    if mode == 'commit':
        insert = insert_commits_raw
    elif mode == 'status':
        insert = insert_status
    elif mode == 'perplexity':
        insert = insert_perplexity
    elif mode == 'lookup-sha':
        lookup = 'sha'
    else:
        print('[mode] must be lookup-sha, commit, status, or perplexity',
              file=sys.stderr)
        sys.exit(-1)

    if insert is not None:
        do_insert_from_csv(insert, argument)
    else:
        commit = fetch_commit_by_sha(argument)
        print(commit)
        print(commit.tokens_as_string)
