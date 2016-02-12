#!/usr/bin/python -i

import re
import pickle
from random import shuffle

import commit

with open('./commits.pickle', 'rb') as fp:
    repos = pickle.load(fp)

template = r'''
<article class="commit{language_class}{empty_class}">
    <section class="message">
        {commit.message}
    </section>

    <section class="tokens">
        {tokens}
    </section>
</article>
'''


def is_special(text):
    return bool(re.match(r'[A-Z]', text))


def htmlize_tokens(tokens):
    def generate_spans():
        for token in tokens:
            classes = ['token']
            if is_special(token):
                classes.append('special-token')

            yield ('<span class="{classes}">{text}</span>'\
                   .format(classes=' '.join(classes),
                           text=token))

    return ' '.join(span for span in generate_spans())

print("""\
<html>
<head>
    <link rel="stylesheet" href="styles.css">
</head>
<body>\
""")

def commits():
    for repo, commits in repos.items():
        for commit in commits:
            yield commit

def print_commit(commit):
    print(template.format(commit=commit,
                          tokens=htmlize_tokens(commit.tokens),
                          language_class=' english' if commit.is_plausibly_english else '',
                          empty_class=' empty' if commit.is_empty else ''))

all_commits = list(commits())
shuffle(all_commits)
for n, commit in enumerate(all_commits):
    if n >= 1000:
        break
    print_commit(commit)
