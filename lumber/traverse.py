from os import listdir
from os.path import exists, join
from dulwich.repo import Repo, NotGitRepository

def traverse_local(work, central):
    """Yield (local repo object, central repo object) tuples for each 
    local repository.

    :param work: root of working repositories
    :param central: root of central repositories
    """
    for repo in sorted(listdir(central)):
        workpath = join(work, repo[:-4])
        if not exists(workpath):
            continue
        try:
            yield Repo(workpath), Repo(join(central, repo))
        except NotGitRepository:
            continue
