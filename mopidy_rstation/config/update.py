# encoding=utf8
import subprocess
from settings import Config

MEDIA_REMOTE_URL = Config.get_config()['media_remote_url']
APP_SOURCE_REMOTE_URL = Config.get_config()['app_source_remote_url']
MEDIA_DIR = Config.get_config()['media_dir']
APP_SOURCE_DIR = Config.get_config()['app_source_dir']
C_APP = 'APP'
C_MEDIA = 'MEDIA'


def git(*args):
    ret = subprocess.check_output(['git'] + list(args))
    print('git ' + str(list(args)))
    return ret


def pip(*args):
    ret = subprocess.check_output(['pip'] + list(args))
    return ret


def isUpToDate(repo_dir):
    # git fetch origin
    git("--git-dir=" + repo_dir + "/.git", "fetch", 'origin', 'master')
    sha1_rev_local = ''
    sha1_rev_remote = ''
    # local VS remote
    # git rev-parse @ VS git rev-parse @{u}
    sha1_rev_local = git(
        "--git-dir=" + repo_dir + "/.git", "rev-parse", '@')
    sha1_rev_remote = git(
        "--git-dir=" + repo_dir + "/.git", "rev-parse", '@{u}')

    if sha1_rev_local == sha1_rev_remote:
        return True
    else:
        return False


def needToPull(repo_dir):
    sha1_rev_local = ''
    sha1_rev_base = ''
    # local VS base
    # git rev-parse @ VS git merge-base @ @{u}
    sha1_rev_local = git(
        "--git-dir=" + repo_dir + "/.git", "rev-parse", '@')
    sha1_rev_base = git(
        "--git-dir=" + repo_dir + "/.git", "merge-base", '@', '@{u}')
    if sha1_rev_local != sha1_rev_base:
        # Need to pull
        return True
    else:
        return False


def needToPush(repo_dir):
    sha1_rev_remote = ''
    sha1_rev_base = ''
    # remote VS base
    # git rev-parse @ VS git rev-parse @{u}
    sha1_rev_remote = git(
        "--git-dir=" + MEDIA_DIR + "/.git", "rev-parse", '@{u}')
    sha1_rev_base = git(
        "--git-dir=" + repo_dir + "/.git", "merge-base", '@', '@{u}')
    # Need to push
    if sha1_rev_remote != sha1_rev_base:
        return True
    else:
        return False


def pull(repo):
    # TODO reset --hard HEAD
    if repo == C_MEDIA:
        git("--git-dir=" + MEDIA_DIR + "/.git",
            "pull", MEDIA_REMOTE_URL)
    elif repo == C_APP:
        git("--git-dir=" + APP_SOURCE_DIR + "/.git",
            "pull", APP_SOURCE_REMOTE_URL)


def resetHard(repo):
    # git reset --hard FETCH_HEAD
    if repo == C_MEDIA:
        git("--git-dir=" + MEDIA_DIR + "/.git",
            "reset", '--hard', 'FETCH_HEAD')
        # ("--git-dir=" + MEDIA_DIR + "/.git",
        #     "clean", "-df")
    elif repo == C_APP:
        git("--git-dir=" + APP_SOURCE_DIR + "/.git",
            "reset", '--hard', 'FETCH_HEAD')
        # ("--git-dir=" + MEDIA_DIR + "/.git",
        #     "clean", "-df")


def updateApp():
    ret = pip('install', APP_SOURCE_DIR, '-U')
    print(ret)


def restartService():
    command = ['systemctl', 'restart', 'mopidy']
    # shell=FALSE for sudo to work.
    subprocess.call(command, shell=False)


def main(git_dir):
    if isUpToDate(git_dir):
        print(git_dir + ' Is up to date!')
    else:
        print(git_dir + ' Is NOT up to date!')
    if needToPull(git_dir):
        print(git_dir + ' Need to pull!')
    else:
        print(git_dir + ' NO need to pull!')
    if needToPush(git_dir):
        print(git_dir + ' Need to push!')
    else:
        print(git_dir + ' NO need to push!')

if __name__ == '__main__':
    print('--- APP ---')
    main(APP_SOURCE_DIR)
    print('--- MEDIA ---')
    main(MEDIA_DIR)
