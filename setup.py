from distutils.core import setup

setup(name='lumber',
      keywords='git',
      version='0.1',
      license='GPLv2',
      author='Dickon Reed',
      author_email='dickon@cantab.net',
      long_description='Work out unpulled and unpushed commits '
      'across local copies of a set of git repositories.',
      scripts=['lumber-status'])

