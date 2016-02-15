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

import os
import re
import sqlite3
from datetime import datetime

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

    PRIMARY KEY (repo, sha) ON CONFLICT ABORT
) WITHOUT ROWID;

-- Travis-CI
CREATE TABLE IF NOT EXISTS
status_check (
    repo    TEXT NOT NULL,
    sha     TEXT NOT NULL,

    -- Insertion date.
    time    DATE NOT NULL,

    -- The actual status!
    status  TEXT NOT NULL,

    PRIMARY KEY (repo, sha)
) WITHOUT ROWID;

-- Leave-one-out perplexity
CREATE TABLE IF NOT EXISTS
perplexity (
    repo    TEXT NOT NULL,
    sha     TEXT NOT NULL,

    -- Insertion date.
    time    DATE NOT NULL,

    -- The actual perplexity!
    perplexity  REAL NOT NULL,

    PRIMARY KEY (repo, sha)
) WITHOUT ROWID;

CREATE VIEW IF NOT EXISTS
repositories (
    name    TEXT,
    len     INTEGER
)
AS SELECT DISTINCT repo AS name, COUNT(sha)
FROM commits;

CREATE VIEW IF NOT EXISTS
commits (
    repo        TEXT,
    sha         TEXT,
    time        DATE,
    message     TEXT,
    status      TEXT,
    perplexity  REAL
)
AS SELECT
    c.repo AS repo, c.sha AS sha,
    c.time AS time, c.message AS message,
    status, perplexity
FROM
    commits_raw AS c
    JOIN status_check   USING (repo, sha)
    JOIN perplexity     USING (repo, sha)
WHERE
    status IS NOT 'cancelled';

-- Look-up a commit by SHA; there's an insignificant non-zero possibilty of a
-- collision, so we assume they are unique.
CREATE UNIQUE INDEX IF NOT EXISTS
commit_sha ON commits_raw (sha);
"""

FILENAME = os.getenv('COMMIT_DATABASE',
                     os.path.join(os.path.dirname(__file__),
                                  'commits.sqlite'))

# Connect initially, and create the schema.
conn = sqlite3.connect(FILENAME)
conn.execute(SCHEMA)

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
        ''', repo, sha, time, message)


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

    return Commit(*cursor.fetchone())


def fetch_commit_by_sha(sha):
    cursor = conn.execute('''
        SELECT
            repo, sha, time, message, status, perplexity
        FROM commits
        WHERE
            sha = ?
    ''', (sha,))

    return Commit(*cursor.fetchone())


def insert_status(repo, sha, status):
    """
    Persist a build status.
    """

    with conn:
        conn.execute('''\
            INSERT INTO status_check (
                repo, sha, time, status
            ) VALUES (?, ?, datetime('now'), ?)
        ''', repo, sha, status)


def insert_perplexity(repo, sha, perplexity):
    """
    Persist perplexity.
    """

    with conn:
        conn.execute('''\
            INSERT INTO status_check (
                repo, sha, time, status
            ) VALUES (?, ?, datetime('now'), ?)
        ''', repo, sha, status)
