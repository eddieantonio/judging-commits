 - [x] Tokenize every commit message, by project. Pickle.
 - [x] Download data from Travis-CI, ~~GHTorrent~~.
 - [x] For each project: train model on all projects other than
        current.
 - [ ] Do cross-folds validation.
 - [ ] ~~Validate the model against each project -- one-way ANOVA should
       say it's not different.~~
 - [ ] If everything checks out -- assumption is that no one project's
       model is sufficiently different, then we're in business!
 - [ ] Manually classify a random sample of commits.

Install on Ubuntu:

    $ sudo apt-get install -y build-essential python3-dev python-virtualenv
    $ virtualenv challenge -p `which python3`
    $ source challenge/bin/activate
    (challenge) $ pip install -r requirements
    $ bundle install

MITLM:

    $ sudo apt-get install build-essential autoconf gfortran libtool
    $ curl -OL https://github.com/eddieantonio/mitlm/archive/v0.4.2.tar.gz
    $ tar xzf v0.4.2.tar.gz
    $ cd mitlm
    $ ./autogen.sh
    $ make

