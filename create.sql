DROP TABLE IF EXISTS commits;
DROP TABLE IF EXISTS repositories;
DROP TABLE IF EXISTS did_status_check;

CREATE TABLE repositories (
    repo TEXT NOT NULL,
    sha TEXT NOT NULL,

    PRIMARY KEY (repo, sha)
);

CREATE TABLE commits (
    repo TEXT NOT NULL,
    sha TEXT NOT NULL,

 -- Very denormalized:
    time DATE NOT NULL,
    message TEXT NOT NULL,

 -- Inserted by Travis-CI
    build_status TEXT,
 -- Inserted by language model
    perplexity REAL,

    PRIMARY KEY (repo, sha) ON CONFLICT ABORT
) WITHOUT ROWID;

CREATE TABLE did_status_check (
    repo TEXT NOT NULL,
    sha TEXT NOT NULL,

    time DATE NOT NULL,

    PRIMARY KEY (repo, sha)
);
