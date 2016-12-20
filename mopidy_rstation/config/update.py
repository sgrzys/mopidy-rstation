# encoding=utf8
import subprocess
from settings import Config

MEDIA_REMOTE_URL = Config.get_config()['media_remote_url']
APP_SOURCE_REMOTE_URL = Config.get_config()['app_source_remote_url']
MEDIA_DIR = Config.get_config()['media_dir']
APP_SOURCE_DIR = Config.get_config()['app_source_dir']
C_APP = 'APP'
C_MEDIA = 'MEDIA'


def git(repo_dir, *args):
    ret = subprocess.check_output(['git'] + list(args), cwd=repo_dir)
    print('git ' + str(list(args)))
    return ret


def pip(*args):
    ret = subprocess.check_output(['pip'] + list(args))
    return ret


def isUpToDate(repo_dir):
    # git fetch origin
    # "--git-dir=" + repo_dir + "/.git"
    git(repo_dir, "fetch", 'origin', 'master')
    sha1_rev_local = ''
    sha1_rev_remote = ''
    # local VS remote
    # git rev-parse @ VS git rev-parse @{u}
    sha1_rev_local = git(repo_dir, "rev-parse", '@')
    sha1_rev_remote = git(repo_dir, "rev-parse", '@{u}')

    if sha1_rev_local == sha1_rev_remote:
        return True
    else:
        return False


def needToPull(repo_dir):
    sha1_rev_local = ''
    sha1_rev_base = ''
    # local VS base
    # git rev-parse @ VS git merge-base @ @{u}
    sha1_rev_local = git(repo_dir, "rev-parse", '@')
    sha1_rev_base = git(repo_dir, "merge-base", '@', '@{u}')
    if sha1_rev_local != sha1_rev_base:
        # Need to pull
        return True
    else:
        return False


def needToPush(repo_dir):
    sha1_rev_remote = ''
    sha1_rev_base = ''
    # remote VS baseMEDIA_REMOTE_URL
    # git rev-parse @ VS git rev-parse @{u}
    sha1_rev_remote = git(repo_dir, "rev-parse", '@{u}')
    sha1_rev_base = git(repo_dir, "merge-base", '@', '@{u}')
    # Need to push
    if sha1_rev_remote != sha1_rev_base:
        return True
    else:
        return False


def pull(repo_dir):
    git(repo_dir, "pull")


def resetHard(repo_dir):
    # git reset --hard FETCH_HEAD
    git(repo_dir, "reset", '--hard', 'FETCH_HEAD')


def updateApp():
    ret = pip('install', APP_SOURCE_DIR, '-U')
    print(ret)


def restartService():
    command = ['pkill', '-9', 'mopidy']
    subprocess.call(command, shell=False)
    command = ['systemctl', 'restart', 'mopidy']
    subprocess.call(command, shell=False)


def get_version_info(repo_dir):
    return git(repo_dir, "log", "-1", "--pretty=format:'%s %cr %an'")


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
    # print('--- APP ---')
    # main(APP_SOURCE_DIR)
    # print('--- MEDIA ---')
    # main(MEDIA_DIR)
    if isUpToDate(MEDIA_DIR):
        print('MEDIA_UP_TO_DATE')
    else:
        resetHard(MEDIA_DIR)
        print('MEDIA_UPDATED')
