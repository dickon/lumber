"""Lumber options and config file handling"""

from optparse import OptionParser
from ConfigParser import RawConfigParser, NoOptionError, NoSectionError
from os import getcwd
from os.path import expanduser

OPTIONS = [('w', 'work', 'paths', getcwd(), 'DIRECTORY',
            """Work repositories are in DIRECTORY."""),
           ('c', 'central', 'paths', None, 'DIRECTORY',
            """Central repositories are in DIRECTORY."""),
           ('b', 'branch', 'general', 'master', 'BRANCH', 'Look at BRANCH.'),
           ('v', 'verbose', 'general', False, 'BOOLEAN', 'Show debug output.')]

def read_options():
    """Read options"""
    config = RawConfigParser()
    config.read(expanduser('~/.lumberrc'))
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
    return parser.parse_args()
