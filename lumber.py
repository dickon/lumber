#! /usr/bin/env python

from dulwich.repo import Repo
from os import listdir
from os.path import join, exists, expanduser
from time import strftime, gmtime, time, asctime, localtime
from math import floor, log10
from ConfigParser import RawConfigParser
from subprocess import Popen, PIPE
CONFIG = RawConfigParser()
CONFIG.read(expanduser('~/.lumberrc'))
SOURCE_DIRECTORY = CONFIG.get('paths', 'central')
LOCAL_CHECKOUTS_DIRECTORY = CONFIG.get('paths', 'work')
BRANCH = CONFIG.get('general', 'branch')
LIMIT = CONFIG.getint('search', 'limit')
VERBOSE = CONFIG.getboolean('search', 'verbose')
repos = sorted(listdir(SOURCE_DIRECTORY))
longest = max( *[len(repo) for repo in repos])

def sigfigs(num, sig_figs):
    if num != 0:
        x = round(num, -int(floor(log10(abs(num))) - (sig_figs - 1)))
        if x == int(x):
            return str(int(x))
        else:
            return str(x)
    else:
        return 0  # Can't take the log of 0

def search_back(repo, predicate, start):
    if VERBOSE:
        print repo.path, 'iterate start at', start
    for depth, entry in enumerate(repo.get_walker(max_entries=LIMIT,
                                                  include=[start])):
        if VERBOSE:
            print repo.path, depth, 'at', entry.commit.id[:8]
        if predicate(entry.commit.id):
            if VERBOSE:
                print repo.path, entry.commit.id[:8], 'accepted'
            return depth
    if VERBOSE:
        print repo.path, 'iteration stopped'
    return 'many'

def pad(text, length):
    """Pad text out to length using spaces on the left"""
    return (' '*max(0, length-len(text)))+text

def run_no_check(command, cwd=None):
    """Run command in cwd, return stdout. Ignore non-zero exit codes"""
    process = Popen(command, cwd=cwd, stdout=PIPE)
    stdout, _ = process.communicate()
    return stdout

for word in repos:
    path = join(SOURCE_DIRECTORY, word)
    lpath = join(LOCAL_CHECKOUTS_DIRECTORY, word[:-4])
    local = exists(lpath)
    if not local or not word.endswith('.git'):
        continue
    central_repo = Repo(path)
    try:
        master = central_repo[central_repo.ref('refs/heads/'+BRANCH)]
    except KeyError:
        continue
    print pad(word[:-4], longest),
    lrepo = Repo(lpath)
    lmaster = lrepo.ref('refs/heads/'+BRANCH)
    unpulled = search_back(central_repo, lambda x: x in lrepo, master.id)
    if not unpulled:
        print '(up to date)',
    else:
        print 'unpulled='+str(unpulled) + ('+' if unpulled == LIMIT else ''),
    lindex = lrepo.open_index()
    difflines = len(run_no_check(['git', 'diff'], cwd=lpath).split('\n')) - 1
    if difflines:
        print 'diff_lines=%d' % (difflines),
    changes = list(lindex.changes_from_tree(lrepo.object_store, 
                                            lrepo['HEAD'].tree))
    
    if changes:
        print 'staged_files=%d' % (len(changes)),
    unpushed = search_back(lrepo, lambda x: x in central_repo, lmaster)
    if unpushed:
        print 'unpushed='+str(unpushed),
    print







