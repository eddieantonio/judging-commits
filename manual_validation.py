#!/usr/bin/env python3

import os
import pickle
import random
import sys
import termios
import textwrap
import tty

from blessings import Terminal
from commit import Commit
import datetime

def singleton(cls):
    cls.__str__ = lambda self: cls.__name__
    return cls()

@singleton
class ForeignLanguage: pass
@singleton
class Usual: pass
@singleton
class Unusual: pass

class Input(object):
    MAPPING = {
        ' ': Usual,
        'a': ForeignLanguage,
        'f': Unusual
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
        print("{t.bold}{message}{t.normal}".format(message=message,
                                                   t=self.term))

    def print_prompt(self):
        print("[{t.green}space{t.normal}] Usual "
              "[{t.red}f{t.normal}] Unusual "
              "[{t.yellow}a{t.normal}] Foreign "
              "{t.blue}>>>{t.normal}".format(t=self.term),
              end='')
        sys.stdout.flush()

    def ask_about(self, commit):
        self.print_message(commit)
        self.print_prompt()
        symbol = self.input.next()
        print('', symbol)
        print()
        return symbol


def random_sample(repos):
    n_samples = len(repos)
    all_commits = list(commit
                       for commits in repos.values()
                       for commit in commits)
    random.shuffle(all_commits)
    return all_commits[:n_samples]

if __name__ == '__main__':
    with open('./commits.pickle', 'rb') as fp:
        repos = pickle.load(fp)

    sample = random_sample(repos)

    prompt = Prompt()
    with open('manual-sample.csv', 'w', encoding='UTF-8') as output:
        for commit in sample:
            answer = prompt.ask_about(commit)
            print(commit.repo, commit.sha, answer, sep=',', file=output)
