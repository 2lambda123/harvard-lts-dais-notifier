import logging, traceback

from git import Repo, GitError

from app.health.exceptions.get_current_commit_hash_exception import GetCurrentCommitHashException


class GitService:
    __PATH_TO_REPO = "/home/appuser"

    def get_current_commit_hash(self) -> str:
        """
        Retrieves current repository commit hash.

        :raises GetCurrentCommitHashException
        """
        logger = logging.getLogger('dais-notifier')
        try:
            logger.info("Obtaining current git commit hash...")
            repo = Repo(self.__PATH_TO_REPO)
            commit_hash = repo.git.rev_parse("HEAD")
            logger.info("Current git commit hash: " + commit_hash)
            return commit_hash
        except GitError as ge:
            logger.error(traceback.format_exc())
            raise GetCurrentCommitHashException(traceback.format_exc())
