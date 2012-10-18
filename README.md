lumber
======

Work out unpulled and unpushed commits across local copies of a set of git
repositories.


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

