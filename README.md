lumber
======

Work out unpulled and unpushed commits across local copies of a set of git
repositories.

Example output
==============

   $ lumber-status -c /path/to/my/central/repos 

                                  blktap (up to date)
                           build-scripts unpulled=9
                                    docs unpulled=72
                                     idl unpulled=3
                                   input unpulled=2
                               installer unpulled=8
                         linux-2.6.32-pq unpulled=1
                                 manager unpulled=146
                                 scripts (up to date)
                          selinux-policy unpulled=43
                                sync-cli (up to date)
                             sync-client (up to date) diff_lines=11 staged_files=1 unpushed=1
                           sync-database (up to date)
                             sync-server (up to date)
                          toolstack-data unpulled=9
                               toolstack unpulled=5
 

   $ lumber-status -c /path/to/my/central/repos git pull

Installation
============

    sudo python setup.py install

Configuration
=============

See lumber-status --help. There is support for a config file at ~/.lumberrc, such as:

    [paths]
    central = /my/project/central/git/repos
    work = /scratch/src

    [general]
    branch=master

    [search]
    limit=500
    verbose=no


Dependencies
============

 * python (developed on Python 2.6)
 * dulwich from http://www.samba.org/~jelmer/dulwich/. Developed against 0.8.5 
   though other versions might work.

