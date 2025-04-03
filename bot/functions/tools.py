import contextlib
import os
import shutil

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from bot import Config
from bot.core import LOGS


async def restart(
        update: bool = False,
        clean_up: bool = False,
        shutdown: bool = False,
):
    try:
        shutil.rmtree(Config.DWNL_DIR)
    except BaseException as e:
        LOGS.info(f"{e}")

    if clean_up:
        os.system(f"mkdir {Config.DWNL_DIR}")
        return

    if shutdown:
        return os.system(f"kill -9 {os.getpid()}")

    cmd = (
        "git pull && pip3 install -U -r requirements.txt && bash start.sh"
        if update
        else "bash start.sh"
    )

    os.system(f"kill -9 {os.getpid()} && {cmd}")

async def init_git(git_rep: str):
    force = False
    try:
        repo = Repo()
    except NoSuchPathError as path_err:
        repo.__del__()
        return False, path_err, force
    except GitCommandError as git_err:
        repo.__del__()
        return False, git_err, force
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", f"https://github.com/{git_rep}")
        origin.fetch()
        repo.create_head("main", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
        force = True

    try:
        origin = repo.remotes["upstream"]
        origin.set_url(f"https://github.com/{git_rep}")
    except KeyError:
        with contextlib.suppress(ValueError, RuntimeError):
            repo.create_remote("upstream", f"https://github.com/{git_rep}")

    return True, repo, force



