lumber
======

Work out unpulled and unpushed commits across local copies of a set of git
repositories.


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

python 
dulwich from http://www.samba.org/~jelmer/dulwich/

