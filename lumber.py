#! /usr/bin/env python

from dulwich.repo import Repo, NotGitRepository
from os import listdir, getcwd
from os.path import join, exists, expanduser, split
from sys import stderr
from math import floor, log10
from ConfigParser import RawConfigParser, NoOptionError, NoSectionError
from subprocess import Popen, PIPE
from optparse import OptionParser

OPTIONS = [('w', 'work', 'paths', getcwd(), 'DIRECTORY',
            """Work repositories are in DIRECTORY."""),
           ('c', 'central', 'paths', None, 'DIRECTORY',
            """Central repositories are in DIRECTORY."""),
           ('b', 'branch', 'general', 'master', 'BRANCH', 'Look at BRANCH.'),
           ('v', 'verbose', 'general', False, 'BOOLEAN', 'Show debug output.')]

def sigfigs(num, sig_figs):
    if num != 0:
        x = round(num, -int(floor(log10(abs(num))) - (sig_figs - 1)))
        if x == int(x):
            return str(int(x))
        else:
            return str(x)
    else:
        return 0  # Can't take the log of 0

def search_back(repo, predicate, start, limit=None):
    for depth, entry in enumerate(repo.get_walker(max_entries=limit,
                                                  include=[start])):
        if predicate(entry.commit.id):
            return depth
    return 'many'

def pad(text, length):
    """Pad text out to length using spaces on the left"""
    return (' '*max(0, length-len(text)))+text

def run_no_check(command, cwd=None):
    """Run command in cwd, return stdout. Ignore non-zero exit codes"""
    process = Popen(command, cwd=cwd, stdout=PIPE)
    stdout, _ = process.communicate()
    return stdout

def scan_repo(branch, work_path, central_path, longest=32):
    """Scan repository locally and remotely and return a summary string.

    :param branch: branch to consider
    :param work_path: path of work repository
    :param central_path: path of central repository
    :param longest: assume at most this many characaters in the repository
    """
    local = exists(work_path)
    if not local:
        return
    try:
        central_repo = Repo(central_path)
    except NotGitRepository:
        return
    try:
        master = central_repo[central_repo.ref('refs/heads/'+branch)]
    except KeyError:
        return
    out = pad(split(work_path)[1], longest)+ ' '
    lrepo = Repo(work_path)
    lmaster = lrepo.ref('refs/heads/'+branch)
    unpulled = search_back(central_repo, lambda x: x in lrepo, master.id,
                           limit=longest)
    if not unpulled:
        out += '(up to date) '
    else:
        out += 'unpulled='+str(unpulled) + ('+' if unpulled == longest 
                                            else '') + ' '
    lindex = lrepo.open_index()
    difflines = len(run_no_check(['git', 'diff'], 
                                 cwd=work_path).split('\n')) - 1
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

def read_options():
    """Read options"""
    config = RawConfigParser()
    config.read(expanduser('~/.lumberrc2'))
    parser = OptionParser()
    for short, option, section, default, metavar, helptext in OPTIONS:
        sectiontext = ' Configure in ~/.lumberrc as %s in %s section.' % (
            option, section)
        try:
            if type(default) == type(True):
                action = 'store_true'
                cdefault = config.getboolean(section, option)
            else:
                action = 'store'
                cdefault = config.get(section, option)
        except (NoOptionError, NoSectionError):
            cdefault = default
        parser.add_option('-'+short, '--'+option, dest=option,
                          action=action,
                          default=cdefault, metavar=metavar,
                          help=helptext + sectiontext)
    options, args = parser.parse_args()
    return options

def main():
    """Entry point"""
    options = read_options()
    if options.central is None:
        print >>stderr, 'ERROR: no central repository directory; configure with -c or config file'
        exit(1)
    repos = sorted(listdir(options.central))
    longest = max( *[len(repo) for repo in repos])
    for repo in repos:
        out = scan_repo(options.branch,
                        join(options.work, repo[:-4]),
                        join(options.central, repo), longest)
        if out:
            print out

if __name__ == '__main__':
    main()




