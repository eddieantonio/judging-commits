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

