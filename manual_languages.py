#!/usr/bin/env python3

import datetime
import os
import pickle
import random
import sys
import termios
import textwrap
import tty

from blessings import Terminal
from tqdm import tqdm

import persist
from commit import Commit


def singleton(cls):
    cls.__str__ = lambda self: cls.__name__
    return cls()

@singleton
class ForeignLanguage: pass
@singleton
class English: pass
@singleton
class RestAllEnglish: pass

class Input(object):
    MAPPING = {
        'j': ForeignLanguage,
        'k': English,
        '>': RestAllEnglish
    }

    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())

        return self

    def __exit__(self, execption, exec_type, traceback):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def next(self):
        symbol = None
        with self:
            while symbol is None:
                ch = sys.stdin.read(1)
                assert len(ch) == 1
                symbol = self.MAPPING.get(ch, None)
        return symbol


class Prompt(object):
    def __init__(self):
        assert sys.stdout.isatty()
        self.input = Input()
        self.term = Terminal()

    def print_message(self, commit):
        formatter = textwrap.TextWrapper(width=self.term.width - 8,
                                         initial_indent='    ')
        message = formatter.fill(commit.message)
        print("{message}".format(message=message,
                                 t=self.term))

    def print_prompt(self):
        print("[{t.green}j{t.normal}] Not English "
              "[{t.yellow}k{t.normal}] English "
              "[{t.red}>{t.normal}] All the rest are English "
              "{t.blue}>>>{t.normal}".format(t=self.term),
              end='')
        sys.stdout.flush()

    def ask_about(self, title, commits):
        print("{t.bold}{title}{t.normal".format(title=title,
                                                t=self.term))
        for commit in commits:
            self.print_message(commit)

        self.print_prompt()
        symbol = self.input.next()
        print('', symbol)
        print()
        return symbol


def english_score_average(repository):
    commits = persist.fetch_commits_by_repo(repository)

    valid_commits = [commit for commit in commits if commit.is_valid]
    if not valid_commits:
        return None

    n = 0
    score = 0.0
    for commit in valid_commits:
        n += 1
        lang, confidence = commit.most_likely_language
        if lang == 'en':
            score += confidence

    return repository, valid_commits, score / n


if __name__ == '__main__':
    # Get all elligible repos
    repos = list(persist.fetch_elligible_repositories())

    # Fetch all of the commits.
    with_averages = (english_score_average(r) for r in repos)
    # For each repo, calculate its language score average
    repo_commits = list(tqdm((repo, commits) for repo, commits, _ in
                             with_averages if repo is not None))
    repo_commits.sort(key=lambda t: t[2])

    print("Found", len(repo_commits), "elligible repositories")

    prompt = Prompt()
    all_rest_english = False
    for repo, commits in repo_commits:
        if all_rest_english:
            persist.set_project_langauge(repo, 'en')
        else:
            random.shuffle(commits)
            answer = prompt.ask_about(repo, commits[:3])

            if answer is RestAllEnglish:
                all_rest_english = True
                answer = English

            if answer is English:
                persist.set_project_langauge(repo, 'en')
            elif answer is ForeignLanguage:
                # Do not insert.
                pass
            else:
                assert False, "Something bad happend."
