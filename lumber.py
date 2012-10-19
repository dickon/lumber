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

def scan_repo(repo, longest=32):
    """Scan repository locally and remotely and return a summary string.

    :param repo: name of remote repository including .git extension
    :param longest: assume at most this many characaters in the repository
    """
    path = join(SOURCE_DIRECTORY, repo)
    lpath = join(LOCAL_CHECKOUTS_DIRECTORY, repo[:-4])
    local = exists(lpath)
    if not local or not repo.endswith('.git'):
        return
    central_repo = Repo(path)
    try:
        master = central_repo[central_repo.ref('refs/heads/'+BRANCH)]
    except KeyError:
        return
    out = pad(repo[:-4], longest)+ ' '
    lrepo = Repo(lpath)
    lmaster = lrepo.ref('refs/heads/'+BRANCH)
    unpulled = search_back(central_repo, lambda x: x in lrepo, master.id)
    if not unpulled:
        out += '(up to date) '
    else:
        out += 'unpulled='+str(unpulled) + ('+' if unpulled == LIMIT else '') + ' '
    lindex = lrepo.open_index()
    difflines = len(run_no_check(['git', 'diff'], cwd=lpath).split('\n')) - 1
    if difflines:
        out += 'diff_lines=%d ' % (difflines)
    changes = list(lindex.changes_from_tree(lrepo.object_store, 
                                            lrepo['HEAD'].tree))
    
    if changes:
        out += 'staged_files=%d ' % (len(changes))
    unpushed = search_back(lrepo, lambda x: x in central_repo, lmaster)
    if unpushed:
        out += 'unpushed='+str(unpushed)+ ' '
    return out

def main():
    repos = sorted(listdir(SOURCE_DIRECTORY))
    longest = max( *[len(repo) for repo in repos])
    for repo in repos:
        out = scan_repo(repo, longest)
        if out:
            print out

if __name__ == '__main__':
    main()




