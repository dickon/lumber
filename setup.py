from distutils.core import setup

setup(name='Lumber',
      keywords='git',
      version='0.1',
      license='GPLv2',
      author='Dickon Reed',
      author_email='dickon@cantab.net',
      requires=['dulwich'],
      packages=['lumber'],
      long_description=open('README.md').read(),
      description='Work out unpulled and unpushed commits '
      'across local copies of a set of git repositories.',
      scripts=['bin/lumber-status'])
