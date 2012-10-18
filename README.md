lumber
======

Work out unpulled and unpushed commits across local copies of a set of git
repositories.

Example output
==============

                           build-scripts unpulled 9 most recent 7.3d ago
                                    docs unpulled 72 most recent 3.1d ago unpushed 1
                                  icbinn up to date
                                     idl unpulled 3 most recent 21d ago
                                   input unpulled 2 most recent 15d ago
                               installer unpulled 8 most recent 1.2d ago
                         linux-2.6.32-pq unpulled 1 most recent 15d ago
                                 manager unpulled 146 most recent 10h ago
                                 scripts up to date
                          selinux-policy unpulled 43 most recent 5.3h ago
                                sync-cli up to date
                             sync-client up to date unpushed 1
                           sync-database up to date
                             sync-server up to date
 

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

