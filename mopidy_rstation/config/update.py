# encoding=utf8
import subprocess
from settings import Config

REMOTE_URL = Config.get_config()['media_remote_url']
GIT_DIR = Config.get_config()['media_dir']


def git(*args):
    print('start')
    subprocess.check_call(['git'] + list(args))
    print('stop')


def pull_media():
    # git("--git-dir=/home/pi/media/.git", "log")
    # log status
    git("--git-dir=" + GIT_DIR + "/.git", "pull", REMOTE_URL)


def main():
    pull_media()

if __name__ == '__main__':
    main()
