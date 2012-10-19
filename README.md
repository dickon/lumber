lumber
======

Work out unpulled and unpushed commits across local copies of a set of git
repositories.

Example output
==============

                                  blktap (up to date)
                           build-scripts unpulled=9
                                    docs unpulled=72
                                  icbinn (up to date)
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
                                     v4v (up to date)
 

At the moment lumber takes no command line options and its working directory
does not matter, but you need a configuration file.

Configuration
=============

You need a ~/.lumberrc in INI file format, such as:

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
 * dulwich from http://www.samba.org/~jelmer/dulwich/

TODO
====

 * write a setup.py
 * cope with missing fields from config file

