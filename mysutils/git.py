from logging import getLogger
from os.path import exists
from threading import Thread, Event
from typing import Callable, List

try:
    import git
except ImportError:
    raise ModuleNotFoundError('git is required for this command. '
                              'Please, install it with:\n\npip install GitPython~=3.1.11')

logger = getLogger(__name__)


class GitMonitor(object):
    """ A Git monitor to detect changes in a branch. """
    def __init__(self, func: Callable, folder: str, repository: str, branch: str = None, force: bool = False,
                 interval: int = 0) -> None:
        """ Monitor a chatbot data repository.
        :param func: The function to call when the repository changes or
          the first time if the force argument is activated.
        :param folder: The path to the local git repository.
        :param repository: The url to the git repository.
        :param branch: The git branch to monitor. By default, the current branch is used.
        :param interval: The time in seconds to wait before checking for repository changes.
        :param force: If force the update model independently if there are changes in the repository or not.
          If this argument is set, then the model is not copied to the S3 bucket.
        """
        self.func = func
        self.folder = folder
        self.repository = repository
        self.branch = branch if branch else 'master'
        self.force = force
        self.interval = interval
        self.updated = True
        self.__stop = False
        self.__thread = None
        self.__event = Event()

    def monitor(self, update: bool = True, **kwargs) -> None:
        """ Start the monitor.
        :param update: If the local repository is updated after to check changes.
        :param kwargs: Extra arguments to pass to the function.
        """
        force = self.force
        if exists(self.folder):
            repo = git.Repo(self.folder)
        else:
            force = True
            repo = git.Repo.clone_from(self.repository, self.folder)
        if not self.branch:
            self.branch = repo.active_branch.name
        elif repo.active_branch.name != self.branch:
            repo.git.checkout(self.branch)
        updated = True
        while not self.__stop:
            changes = self.__changes(repo)
            if changes or force:
                if update:
                    repo.git.pull()
                    updated = True
                self.func(*changes, **kwargs)
            if not self.interval:
                break
            if updated:
                logger.info(f'Waiting {self.interval}s for changes in the configuration. ')
            self.__event.wait(self.interval)
            force = False
            updated = False
        self.__thread = None
        self.__stop = False

    def __changes(self, repo: git.Repo) -> List[str]:
        """ Get the changes between local and remote repository for the set branch.

        :param repo: The Git repository.
        :return: A list with the changed file names.
        """
        origin = repo.remotes.origin
        fetch = [info for info in origin.fetch() if info.name == f'origin/{self.branch}'][0]
        diff = fetch.commit.diff()
        return [d.a_path for d in diff]

    def start(self, update: bool = True, **kwargs) -> None:
        """ Start the monitor as a thread.

        :param update: If the local repository is updated after to check changes.
        """
        self.__thread = Thread(target=self.monitor, args=(update,), kwargs=kwargs)
        self.__thread.start()

    def stop(self):
        """ Stop the monitor. """
        self.__stop = True
        self.__event.set()
