import os
import shutil
import configparser

from sys import platform
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options, FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager

def get_default_profile():
    if platform == 'linux' or platform == 'linux2':
        mozilla_profile = Path(os.getenv('HOME')) / '.mozilla' / 'firefox'
    elif platform == 'darwin':
        mozilla_profile = Path(os.getenv('HOME')) / \
            'Library' / 'Application Support' / 'Firefox'
    elif platform == 'win32':
        mozilla_profile = Path(os.getenv('APPDATA')) / 'Mozilla' / 'Firefox'

    mozilla_profile_ini = mozilla_profile / 'profiles.ini'
    profile = configparser.ConfigParser()
    profile.read(mozilla_profile_ini)
    return mozilla_profile / profile.get('Profile0', 'Path')


def prepare_sniper_profile(default_profile_path):
    profile = FirefoxProfile(default_profile_path.resolve())
    profile.set_preference('dom.webdriver.enabled', False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    return profile


def create():
    default_profile_path = get_default_profile()
    profile = prepare_sniper_profile(default_profile_path)
    return webdriver.Firefox(firefox_profile=profile, executable_path=GeckoDriverManager().install())
