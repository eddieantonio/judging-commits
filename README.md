Challenge Paper Utilities
=========================

The utilities used to gather and analyze data for

    @article{santos2016,
        title = {Juding a Commit by Its Cover or Can a Commit Message Predict Build Failure},
        shorttitle = {Juding a commit by its cover},
        author = {Santos, Eddie Antonio and Hindle, Abram},
        year = {2016}
    }

Requirements
------------

 - Python 3.4+
    - its libraries installed with pip
    - SQLite 3.8.2+
 - Ruby 1.9+
    - its libraries installed with bundler
 - [MITLM](https://github.com/eddieantonio/mitlm)

Install on OS X
---------------

### Python

    $ brew install python3
    $ sudo pip3 install virtualenv
    $ virtualenv challenge -p `which python3` # or use virtualenvwrapper
    (challenge) $ pip install -r requirements.txt

### Ruby

    $ bundle install

### MITLM

    $ brew tap eddieantonio/eddieantonio
    $ brew install mitlm

Install on Ubuntu
-----------------

### Python

    $ sudo apt-get install -y python3-dev python-pip python-virtualenv
    $ virtualenv challenge -p `which python3` # or use virtualenvwrapper
    $ source challenge/bin/activate
    (challenge) $ pip install -r requirements.txt

### Ruby

    $ sudo apt-get install -y ruby bundler
    $ bundle install

### MITLM

    $ sudo apt-get install build-essential autoconf gfortran libtool
    $ curl -OL https://github.com/eddieantonio/mitlm/archive/v0.4.2.tar.gz
    $ tar xzf v0.4.2.tar.gz
    $ cd mitlm
    $ ./autogen.sh
    $ make -j `nproc`
    $ sudo make install


R Packages
----------

 - ggplot2
 - RSQLite

License
-------

Unless otherwise noted, assume all Python, Ruby, and R sources in this
repository is © 2016 Eddie Antonio Santos, licensed under the Apache 2.0
license.
