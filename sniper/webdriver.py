import os
import shutil
import configparser
import logging

from sys import platform
from pathlib import Path
try:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options, FirefoxProfile
    from webdriver_manager.firefox import GeckoDriverManager
except Exception:
    logging.error(
        'Could not import all required modules. '
        'Please run the following command again:\n\n'
        '\tpipenv install\n')
    exit()


def get_profile_path():
    if platform == 'linux' or platform == 'linux2':
        profile_path = Path(os.getenv('HOME')) / '.mozilla' / 'firefox'
    elif platform == 'darwin':
        profile_path = Path(os.getenv('HOME')) / \
            'Library' / 'Application Support' / 'Firefox'
    elif platform == 'win32':
        profile_path = Path(os.getenv('APPDATA')) / 'Mozilla' / 'Firefox'
    if not profile_path.exists():
        raise FileNotFoundError(
            "Mozilla profile doesn't exist and/or can't be located on this machine.")
    return profile_path


def get_default_profile(profile_path):
    mozilla_profile_ini = profile_path / 'profiles.ini'
    profile = configparser.ConfigParser()
    profile.read(mozilla_profile_ini)
    return profile.get('Profile0', 'Path')


def prepare_sniper_profile(default_profile_path):
    profile = FirefoxProfile(default_profile_path.resolve())
    profile.set_preference('dom.webdriver.enabled', False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    return profile


def create():
    profile_path = get_profile_path()
    default_profile = get_default_profile(profile_path)
    logging.info(f'Launching Firefox using default profile: {default_profile}')
    profile = prepare_sniper_profile(profile_path / default_profile)
    driver = webdriver.Firefox(
        firefox_profile=profile, executable_path=GeckoDriverManager().install())
    if os.path.isfile('./recaptcha_solver-5.7-fx.xpi'):
        logging.info('ReCaptcha solver extension detected and installed')
        extension_path = os.path.abspath("recaptcha_solver-5.7-fx.xpi")
        driver.install_addon(extension_path, temporary=True)
    else:
        logging.info('ReCaptcha solver extension not found')
    return driver
