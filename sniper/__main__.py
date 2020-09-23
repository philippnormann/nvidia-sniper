import os
import json
import shutil
import logging
import colorama
import apprise
import configparser

from pathlib import Path
from time import sleep
from sys import platform

from pick import pick
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options, FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager
import sniper.checkout as checkout

HEADER = f'''
{Fore.GREEN}
███╗   ██╗██╗   ██╗██╗██████╗ ██╗ █████╗     
████╗  ██║██║   ██║██║██╔══██╗██║██╔══██╗    
██╔██╗ ██║██║   ██║██║██║  ██║██║███████║    
██║╚██╗██║╚██╗ ██╔╝██║██║  ██║██║██╔══██║    
██║ ╚████║ ╚████╔╝ ██║██████╔╝██║██║  ██║    
╚═╝  ╚═══╝  ╚═══╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝    
{Fore.RED}
███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ 
██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
███████║██║ ╚████║██║██║     ███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
{Style.RESET_ALL}
'''

src_path = Path(__file__).parent
data_path = src_path.parent / 'data'


def read_json(filename):
    with open(data_path / filename, encoding='utf-8') as json_file:
        return json.load(json_file)


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
    sniper_profile_path = default_profile_path.parent / 'sniper.default-release'

    shutil.rmtree(sniper_profile_path)
    shutil.copytree(default_profile_path, sniper_profile_path, symlinks=True)

    shutil.rmtree(sniper_profile_path / 'datareporting')
    shutil.rmtree(sniper_profile_path / 'extensions')
    shutil.rmtree(sniper_profile_path / 'storage')

    os.remove(sniper_profile_path / 'webappsstore.sqlite')
    os.remove(sniper_profile_path / 'favicons.sqlite')
    os.remove(sniper_profile_path / 'places.sqlite')

    profile = FirefoxProfile(sniper_profile_path.resolve())
    profile.set_preference('dom.webdriver.enabled', False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    return profile


def send_notifications(target_gpu, notification_type, notifications):
    driver.save_screenshot('screenshot.png')
    for name, service in notifications['services'].items():
        logging.info(f'Sending notifications to {name}')
        apobj = apprise.Apprise()
        apobj.add(service['url'])
        title = f"Alert - {target_gpu['name']} {notification_type}"
        msg = notifications[notification_type]['message']
        if service['screenshot']:
            apobj.notify(title=title, body=msg,
                         attach='screenshot.png')
        else:
            apobj.notify(title=title, body=msg)


if __name__ == '__main__':
    colorama.init()
    print(HEADER)

    log_format = '%(asctime)s nvidia-sniper: %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    customer = read_json('customer.json')
    locale = customer['locale']
    notifications = customer['notifications']

    gpu_data = read_json('gpus.json')
    target_gpu, _ = pick(list(gpu_data.keys()),
                         'Which GPU are you targeting?',
                         indicator='=>')

    payment_method, _ = pick(['credit-card', 'paypal'],
                             'Which payment method do you want to use?',
                             indicator='=>')

    auto_submit, _ = pick(['Yes', 'No'],
                          'Do you want to automatically submit the order? (only works with credit card)',
                          indicator='=>',  default_index=1)
    auto_submit = auto_submit == 'Yes'

    timeout, _ = pick([' 2 seconds', ' 4 seconds', ' 8 seconds', '16 seconds', '32 seconds'],
                      'Please choose a timout / refresh interval', indicator='=>', default_index=2)
    timeout = int(timeout.replace('seconds', '').strip())

    default_profile_path = get_default_profile()
    profile = prepare_sniper_profile(default_profile_path)

    driver = webdriver.Firefox(
        firefox_profile=profile, executable_path=GeckoDriverManager().install())

    target_gpu = gpu_data[target_gpu]

    while True:
        logging.info(
            f"Checking {locale} availability for {target_gpu['name']}...")
        checkout.get_product_page(driver, locale, target_gpu)
        gpu_available = checkout.check_availability(driver, timeout)
        if gpu_available:
            logging.info(f"Found available GPU: {target_gpu['name']}")
            if notifications['availability']['enabled']:
                send_notifications(target_gpu, 'availability', notifications)
            added_to_basket = False
            while not added_to_basket:
                logging.info(f'Trying to add to basket...')
                added_to_basket = checkout.add_to_basket(driver, timeout)
                if not added_to_basket:
                    logging.info(f'Add to basket click failed, trying again!')

            logging.info(f'Add to basket click suceeded!')
            if notifications['add-to-basket']['enabled']:
                send_notifications(target_gpu, 'add-to-basket', notifications)
            logging.info('Going to checkout page...')
            checkout.to_checkout(driver, timeout, locale)

            if payment_method == 'credit-card':
                checkout.checkout_guest(driver, timeout, customer, auto_submit)
            else:
                checkout.checkout_paypal(driver, timeout),

            logging.info('Checkout successful!')
            if notifications['checkout']['enabled']:
                send_notifications(target_gpu, 'checkout', notifications)

            if auto_submit:
                checkout.click_recaptcha(driver, timeout)
                order_submitted = checkout.submit_order(driver, timeout)
                if order_submitted:
                    logging.info('Auto buy successfully submitted!')
                    if notifications['submit']['enabled']:
                        send_notifications(target_gpu, 'submit', notifications)
                else:
                    logging.error(
                        'Failed to auto buy! Please solve the reCAPTCHA and submit manually...')
                    if notifications['captcha-fail']['enabled']:
                        send_notifications(
                            target_gpu, 'captcha-fail', notifications)
            break
        else:
            logging.info('GPU currently not available')
